from devvio_util.primitives.address import Address
from devvio_util.primitives.signature import Signature
from devvio_util.primitives.utils import InputBuffer, set_uint64, set_uint8
from devvio_util.primitives.devv_sign import sign_binary, DevvHash
from devvio_util.primitives.transfer import Transfer
from devvio_util.primitives.devv_constants import kLEGACY_ENVELOPE_SIZE, kNODE_SIG_BUF_SIZE, kNODE_ADDR_BUF_SIZE, \
    kSIGNER_LENGTH_OFFSET, kUINT_SIZE, kMIN_PAYLOAD_SIZE, kFLAGS_OFFSET, kOPERATION_OFFSET, kLEGACY_OPERATION_OFFSET, \
    kENVELOPE_SIZE, OpType


class Transaction:
    def __init__(self, raw_blk: InputBuffer = None, is_legacy: bool = None):
        self._tx_offset = None
        self._tx_size = None
        self._payload_size = None
        self._xfer_size = None
        self._signer_size = None
        self._signer = None
        self._is_legacy = None
        self._canonical = None
        self._sig = None
        if raw_blk:
            self.from_buffer(raw_blk, is_legacy)

    def from_buffer(self, buffer: InputBuffer, is_legacy: bool):
        self._tx_offset = buffer.tell()
        if is_legacy:
            self._xfer_size = buffer.get_next_uint64()
            self._payload_size = buffer.get_next_uint64()
            self._tx_size = kLEGACY_ENVELOPE_SIZE + self._xfer_size + self._payload_size + kNODE_SIG_BUF_SIZE
            self._signer_size = kNODE_ADDR_BUF_SIZE
        else:
            self._tx_size = buffer.get_next_uint64()
            self._xfer_size = buffer.get_next_uint64()
            self._payload_size = buffer.get_next_uint64()
            self._signer_size = buffer.get_int(self._tx_offset + kSIGNER_LENGTH_OFFSET, kUINT_SIZE) + 1
            self._signer = Address(buffer.get_bytes(self._tx_offset + kSIGNER_LENGTH_OFFSET, self._signer_size))

        if self._payload_size < kMIN_PAYLOAD_SIZE:
            raise Exception(f"Invalid Transaction: bad payload size {self._payload_size}")

        if not Address.is_valid_addr_size(self._signer_size):
            raise Exception(f"Invalid Transaction: bad signer size {self._signer_size}")

        if not is_legacy:
            flags = buffer.get_int(self._tx_offset + kFLAGS_OFFSET, kUINT_SIZE)
            if flags != 0:
                raise Exception("Invalid Transaction: unknown flags")
            oper = buffer.get_int(self._tx_offset + kOPERATION_OFFSET, kUINT_SIZE)
            if oper >= OpType.NUM_OPS:
                raise Exception("Invalid Transaction: invalid operation")
        else:
            oper = buffer.get_int(self._tx_offset + kLEGACY_OPERATION_OFFSET, kUINT_SIZE)
            if oper >= OpType.NUM_OPS:
                raise Exception("Invalid Transaction: invalid operation")
            self._is_legacy = True
        self._sig = self.get_sig_from_raw_blk(buffer)
        buffer.seek(self._tx_offset)
        self._canonical = buffer.get_next_bytes(self._tx_size)
        if not self._canonical:
            raise Exception(f"Invalid Transaction: buffer too small for tx (< {self._tx_size}")

    def get_sig_from_raw_blk(self, buffer: InputBuffer) -> Signature:
        if self._is_legacy:
            offset = self._tx_offset + kLEGACY_ENVELOPE_SIZE + self._payload_size + self._xfer_size + 1
        else:
            offset = kENVELOPE_SIZE + self._payload_size + self._xfer_size + self._signer_size
        sig_len = self._tx_size - offset
        return Signature(buffer.get_bytes(self._tx_offset + offset, sig_len))

    def get_sig(self) -> Signature:
        if self._is_legacy:
            offset = kLEGACY_ENVELOPE_SIZE + self._payload_size + self._xfer_size + 1
        else:
            offset = kENVELOPE_SIZE + self._payload_size + self._xfer_size + self._signer_size
        return Signature(self._canonical[offset:])

    def get_payload(self) -> str:
        if self._is_legacy:
            offset = kNODE_ADDR_BUF_SIZE + self._xfer_size + self._signer_size
        else:
            offset = kENVELOPE_SIZE + self._xfer_size + self._signer_size
        return self.get_canonical()[offset:offset + self._payload_size].decode('utf-8')

    def get_canonical(self) -> bytes:
        return self._canonical

    def get_hex_str(self) -> str or None:
        if not self._canonical:
            return None
        return self._canonical.hex()

    def __str__(self):
        return self.get_hex_str()

    def __bool__(self):
        return self._sig is not None

    def __eq__(self, other):
        return self._sig == other.get_sig()

    def get_xfers_from_raw_blk(self, buffer: InputBuffer) -> list:
        if not self._is_legacy:
            start_offset = self._tx_offset + kENVELOPE_SIZE + self._signer_size
        else:
            start_offset = self._tx_offset + kLEGACY_ENVELOPE_SIZE
        return Transfer.get_xfers_from_buffer(buffer, start_offset, self._xfer_size)

    def get_xfers(self) -> list:
        buffer = InputBuffer(self._canonical)
        return Transfer.get_xfers_from_buffer(buffer, kENVELOPE_SIZE + self._signer_size, self._xfer_size)

    def get_message_digest(self) -> bytes:
        return self._canonical[:kENVELOPE_SIZE + self._signer_size + self._xfer_size + self._payload_size]

    def pre_signature_init(self, oper, signer: Address, xfers: list, payload: bytes, flags, timestamp):
        self._payload_size = len(payload)

        if self._payload_size < kMIN_PAYLOAD_SIZE:
            raise ValueError(f"Failed to serialize transaction, payload too small ({self._payload_size})")

        self._canonical = bytes()
        self._canonical += set_uint64(self._payload_size)

        if set_uint8(oper) >= OpType.NUM_OPS:
            raise ValueError(f"Invalid Transaction: bad OpType ({oper} >= {OpType.NUM_OPS})")
        self._canonical += set_uint8(oper)
        if flags != 0:
            raise ValueError("Invalid Transaction: unknown flags")
        self._canonical += set_uint8(flags)
        self._canonical += set_uint64(timestamp)
        self._canonical += signer.get_canonical()

        self._xfer_size = 0
        for xfer in xfers:
            self._xfer_size += xfer.get_size()
            self._canonical += xfer.get_canonical()

        self._signer_size = signer.get_size()
        self._tx_size = kENVELOPE_SIZE + self._signer_size + self._xfer_size + self._payload_size \
                        + signer.get_corresponding_sig_size()

        self._canonical = set_uint64(self._tx_size) + set_uint64(self._xfer_size) + self._canonical

    def serialize(self, oper: int, signer: Address, xfers: list,
                  payload: bytes, eckey, keys, flags: int, timestamp: int):
        self.pre_signature_init(oper, signer, xfers, payload, eckey, keys, flags, timestamp)

        # TODO: finish sign_binary()
        self._sig = sign_binary(eckey, DevvHash(self._canonical))
        self._canonical += self._sig

    def get_signer(self) -> Address:
        return self._signer


'''
Address Transaction::getSigner() const {
  if (is_legacy_) {
    uint8_t signer_length = kNODE_ADDR_BUF_SIZE;
    std::vector<byte> signer_bin(canonical_.begin()
        + kLEGACY_SIGNER_LENGTH_OFFSET
        , canonical_.begin() + kLEGACY_SIGNER_LENGTH_OFFSET + signer_length);
    Address signer(signer_bin);
    return signer;
  }
  uint8_t signer_length = canonical_[kSIGNER_LENGTH_OFFSET];
  std::vector<byte> signer_bin(canonical_.begin() + kSIGNER_LENGTH_OFFSET
      , canonical_.begin() + kSIGNER_LENGTH_OFFSET + signer_length + 1);
  Address signer(signer_bin);
  return signer;
}
'''


