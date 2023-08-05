from devvio_util.primitives.signature import Signature
from devvio_util.primitives.address import Address
from devvio_util.primitives.devv_constants import \
    kWALLET_ADDR_SIZE, kNODE_ADDR_SIZE, kNODE_SIG_SIZE, kWALLET_SIG_SIZE, \
    kPEM_PREFIX, kPEM_SUFFIX, kPEM_PREFIX_SIZE, kPEM_SUFFIX_SIZE
from devvio_util.primitives.utils import set_uint8

from hashlib import sha256
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.backends.openssl import backend
from cryptography.hazmat.primitives import serialization as sz
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature
import pkg_resources


class DevvHash:
    def __init__(self, raw_bin: bytes):
        self._hash = None
        if not isinstance(raw_bin, bytes):
            raise Exception(f'Failed to hash {type(raw_bin)} (expected bytes)')
        if raw_bin:
            self._hash = sha256(raw_bin).digest()

    def get_bin(self) -> bytes:
        return self._hash if self._hash else b''

    def get_hex(self) -> str:
        return self._hash.hexdigest() if self._hash else ''


def crypto_sanity_check(pkey: str = None, pub: str or Address = None, aes_pass: str = None) -> tuple:
    if not aes_pass:
        aes_pass = 'password'
    if not pkey:
        ec_key = EcSigner(aes_pass=aes_pass)
        pub = ec_key.get_signer_addr()
        pkey = ec_key.get_pkey()
    msg = DevvHash(b'Testing')
    sign_binary(pkey, pub, msg, aes_pass)
    crypto_version = str(pkg_resources.get_distribution('cryptography'))
    openssl_version = backend.openssl_version_text()
    return openssl_version, crypto_version


def sign_binary(pkey: str, pub: str or Address, msg: DevvHash, aes_pass: str):
    try:
        temp = msg.get_bin()

        pkey_bin = bytes(kPEM_PREFIX + pkey + kPEM_SUFFIX, 'utf-8')
        signer = EcSigner(pkey=pkey_bin,
                          pub=pub, aes_pass=aes_pass)

        sig = signer.sign(temp)
        sig_size = len(sig)

        if sig_size < 80:
            pad_len = kWALLET_SIG_SIZE
        else:
            pad_len = kNODE_SIG_SIZE

        if sig_size < pad_len:
            padding = b''
            for i in range(pad_len - sig_size):
                padding += set_uint8(0)
            sig += padding
        elif sig_size > pad_len:
            sig = sig[:pad_len]
        sig_size = pad_len

        if not Signature.is_valid_sig_size(sig_size):
            raise ValueError(f"Invalid signature size ({sig_size})")
        sig = Signature(sig)

        return sig
    except Exception as e:
        raise RuntimeError(f"Signature procedure failed ({e})")


class EcSigner:
    def __init__(self, pkey: bytes = None, pub: str or Address = None, aes_pass: str = None):
        if not aes_pass:
            raise ValueError('Invalid EcSigner: aes_pass cannot be empty')
        self._alg = ec.ECDSA(SHA256())
        self._curve = None
        self._pem_encryption = None

        if pkey and pub:
            self._pub = pub
            self._pk = pkey
            self._load_ec_key(pub, aes_pass)
        else:
            self._make_ec_key(aes_pass)

    def _make_ec_key(self, aes_pass: str):
        try:
            self._curve = ec.SECP256K1()
            ec_key = ec.generate_private_key(self._curve, backend=default_backend())
            self._pem_encryption = sz.BestAvailableEncryption(bytes(aes_pass, 'utf-8'))
            self._pk = ec_key.private_bytes(
                encoding=sz.Encoding.PEM,
                format=sz.PrivateFormat.PKCS8,
                encryption_algorithm=self._pem_encryption,
            )

            self._pub = ec_key.public_key()
        except Exception as e:
            raise Exception(f'Invalid EcSigner: failed to generate EC key-pair ({e})')

    def _load_ec_key(self, pub: str or Address, aes_pass: str):
        if len(self._pub) == kWALLET_ADDR_SIZE * 2 or len(self._pub) == kWALLET_ADDR_SIZE:
            self._curve = ec.SECP256K1()
        elif len(self._pub) == kNODE_ADDR_SIZE * 2 or len(self._pub) == kNODE_ADDR_SIZE:
            self._curve = ec.SECP384R1()
        else:
            raise ValueError(f'Invalid EcSigner: bad public key length ({len(pub)})')
        if self._curve is None:
            raise ValueError('Invalid EcSigner: failed to generate ec_group')

        # Make private and public keys from the private value + curve
        self._pk = sz.load_pem_private_key(
            self._pk,
            password=bytes(aes_pass, 'utf-8'),
            backend=default_backend()
        )

        self._pem_encryption = None
        self._pub = self._pk.public_key()
        if not isinstance(pub, Address):
            pub = Address(pub)
        if self.get_signer_addr() != pub:
            raise Exception(f'Invalid EcSigner: could not reproduce public key')

    def get_pkey(self) -> str:
        return self._pk.decode('utf-8')[kPEM_PREFIX_SIZE:-kPEM_SUFFIX_SIZE].replace('\n', '')

    def get_pubkey(self) -> str:
        return self._pub.hex()

    def get_signer_addr(self) -> Address:
        return Address(self._pub.public_bytes(sz.Encoding.X962,
                                              sz.PublicFormat.CompressedPoint).hex())

    def sign(self, msg: bytes, verify: bool = True) -> bytes:
        if not msg or not isinstance(msg, bytes):
            raise Exception(f'Invalid signing: cannot sign msg type {type(msg)}')
        sig = self._pk.sign(msg, self._alg)
        if verify and not self.verify(sig, msg):
            raise Exception('Invalid signing: failed sig verification')
        return sig

    def verify(self, sig, msg) -> bool:
        try:
            self._pub.verify(sig, msg, self._alg)
            return True
        except InvalidSignature:
            return False
