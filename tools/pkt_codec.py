#!/usr/bin/env python3
"""
Bo giai ma / ma hoa file Cisco Packet Tracer (.pkt, .pka) phien ban 8.x - 9.x.

Dinh dang file gom 4 lop, ap dung theo thu tu khi GIAI MA:
  1. Khu xao tron:  b[i] = a[L-1-i] ^ ((L * (1 - i)) & 0xFF)      (L = do dai file)
  2. Giai ma:       Twofish che do EAX, key = 16 byte 0x89, iv = 16 byte 0x10,
                    tag xac thuc 16 byte nam o cuoi ban ma
  3. Khu xao tron:  b[i] = a[i] ^ ((L - i) & 0xFF)                (L = do dai sau buoc 2)
  4. Giai nen:      4 byte dau (big-endian) la kich thuoc sau giai nen, phan con lai la zlib

Khi MA HOA thi lam nguoc lai theo thu tu 4 -> 1.

Cach dung:
    python3 tools/pkt_codec.py decode vao.pkt ra.xml
    python3 tools/pkt_codec.py encode vao.xml ra.pkt
    python3 tools/pkt_codec.py selftest vao.pkt

Phu thuoc: mot thu vien dung chung Twofish (libtwofish.so) duoc bien dich tu ma nguon
cua Niels Ferguson (goi PyPI "twofish", tap tin twofish-0.3/twofish.c). Xem
tools/README_tools.md de biet cach bien dich lai.
"""
import ctypes
import os
import sys
import zlib

KEY = bytes([0x89] * 16)
IV = bytes([0x10] * 16)
TAG_LEN = 16
BLOCK = 16


def _load_lib():
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (os.path.join(here, "libtwofish.so"),
                 os.environ.get("LIBTWOFISH", "")):
        if cand and os.path.exists(cand):
            return ctypes.CDLL(cand)
    raise SystemExit(
        "Khong tim thay libtwofish.so. Xem tools/README_tools.md de bien dich, "
        "hoac dat bien moi truong LIBTWOFISH tro toi thu vien."
    )


class _TwofishKey(ctypes.Structure):
    _fields_ = [("s", ctypes.c_uint32 * (4 * 256)), ("K", ctypes.c_uint32 * 40)]


class Twofish:
    """Ma khoi Twofish 128 bit, chi can chieu ma hoa (EAX dung CTR va OMAC)."""

    _lib = None

    def __init__(self, key: bytes):
        if Twofish._lib is None:
            Twofish._lib = _load_lib()
            Twofish._lib.Twofish_initialise()
        self._k = _TwofishKey()
        buf = (ctypes.c_ubyte * len(key)).from_buffer_copy(key)
        Twofish._lib.Twofish_prepare_key(buf, len(key), ctypes.byref(self._k))

    def encrypt_block(self, block: bytes) -> bytes:
        inb = (ctypes.c_ubyte * BLOCK).from_buffer_copy(block)
        outb = (ctypes.c_ubyte * BLOCK)()
        Twofish._lib.Twofish_encrypt(ctypes.byref(self._k), inb, outb)
        return bytes(outb)


def _xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def _double(v: bytes) -> bytes:
    i = int.from_bytes(v, "big") << 1
    if i >> 128:
        i ^= 0x87
    return (i & ((1 << 128) - 1)).to_bytes(BLOCK, "big")


def _cmac(tf: Twofish, msg: bytes) -> bytes:
    k1 = _double(tf.encrypt_block(b"\x00" * BLOCK))
    k2 = _double(k1)
    if msg and len(msg) % BLOCK == 0:
        blocks = [msg[i:i + BLOCK] for i in range(0, len(msg), BLOCK)]
        last = _xor(blocks.pop(), k1)
    else:
        pad = msg + b"\x80" + b"\x00" * (BLOCK - 1 - (len(msg) % BLOCK))
        blocks = [pad[i:i + BLOCK] for i in range(0, len(pad), BLOCK)]
        last = _xor(blocks.pop(), k2)
    x = b"\x00" * BLOCK
    for blk in blocks:
        x = tf.encrypt_block(_xor(x, blk))
    return tf.encrypt_block(_xor(x, last))


def _omac(tf: Twofish, t: int, msg: bytes) -> bytes:
    return _cmac(tf, b"\x00" * (BLOCK - 1) + bytes([t]) + msg)


def _ctr(tf: Twofish, nonce: bytes, data: bytes) -> bytes:
    out = bytearray()
    counter = int.from_bytes(nonce, "big")
    for i in range(0, len(data), BLOCK):
        ks = tf.encrypt_block((counter & ((1 << 128) - 1)).to_bytes(BLOCK, "big"))
        counter += 1
        chunk = data[i:i + BLOCK]
        out += _xor(ks[:len(chunk)], chunk)
    return bytes(out)


def eax_decrypt(key: bytes, iv: bytes, data: bytes):
    tf = Twofish(key)
    n = _omac(tf, 0, iv)
    ct, tag = data[:-TAG_LEN], data[-TAG_LEN:]
    pt = _ctr(tf, n, ct)
    expected = _xor(_xor(n, _omac(tf, 1, b"")), _omac(tf, 2, ct))
    return pt, expected[:TAG_LEN] == tag


def eax_encrypt(key: bytes, iv: bytes, pt: bytes) -> bytes:
    tf = Twofish(key)
    n = _omac(tf, 0, iv)
    ct = _ctr(tf, n, pt)
    tag = _xor(_xor(n, _omac(tf, 1, b"")), _omac(tf, 2, ct))
    return ct + tag[:TAG_LEN]


def _unscramble_outer(data: bytes) -> bytes:
    """Lop xao tron ngoai cung, chieu GIAI MA: out[i] = in[L-1-i] ^ (L * (1 - i))."""
    length = len(data)
    return bytes(data[length - 1 - i] ^ ((length * (1 - i)) & 0xFF) for i in range(length))


def _scramble_outer(data: bytes) -> bytes:
    """Lop xao tron ngoai cung, chieu MA HOA: nghich dao cua _unscramble_outer.

    Day KHONG phai mot phep bien doi tu nghich dao: mat na phu thuoc chi so nen
    khi dao chieu phai thay (L * (1 - i)) bang (L * (2 - L + i)).
    """
    length = len(data)
    return bytes(data[length - 1 - i] ^ ((length * (2 - length + i)) & 0xFF)
                 for i in range(length))


def _scramble_inner(data: bytes) -> bytes:
    length = len(data)
    return bytes(b ^ ((length - i) & 0xFF) for i, b in enumerate(data))


def decode(raw: bytes) -> bytes:
    stage1 = _unscramble_outer(raw)
    stage2, ok = eax_decrypt(KEY, IV, stage1)
    if not ok:
        raise ValueError("Tag xac thuc EAX khong khop: file hong hoac khac dinh dang.")
    stage3 = _scramble_inner(stage2)
    declared = int.from_bytes(stage3[:4], "big")
    xml = zlib.decompress(stage3[4:])
    if len(xml) != declared:
        raise ValueError("Kich thuoc sau giai nen khong khop phan dau file.")
    return xml


def encode(xml: bytes) -> bytes:
    body = len(xml).to_bytes(4, "big") + zlib.compress(xml, 6)
    stage3 = _scramble_inner(body)
    stage2 = eax_encrypt(KEY, IV, stage3)
    return _scramble_outer(stage2)


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 1
    cmd = argv[1]
    if cmd == "decode":
        open(argv[3], "wb").write(decode(open(argv[2], "rb").read()))
    elif cmd == "encode":
        open(argv[3], "wb").write(encode(open(argv[2], "rb").read()))
    elif cmd == "selftest":
        raw = open(argv[2], "rb").read()
        xml = decode(raw)
        again = decode(encode(xml))
        assert again == xml, "Vong lap decode/encode khong bao toan noi dung"
        print("selftest OK: %d byte XML, vong lap bao toan noi dung" % len(xml))
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
