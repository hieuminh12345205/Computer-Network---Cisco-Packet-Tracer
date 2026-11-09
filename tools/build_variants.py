#!/usr/bin/env python3
"""
Dung hai ban mo phong tu file goc, bang cach sua truc tiep cau hinh IOS ben trong .pkt.

  1. CSE3030_2_Nhom6_MinhAn.pkt            - phuong an co ban + va lo hong bao mat thiet bi
  2. CSE3030_2_Nhom6_MinhAn_MoRong_ACL.pkt - phuong an co ban + phan mo rong (ACL, port-security)

Vi sao sua thang vao .pkt chu khong chi sua file .txt: neu chi sua ban xuat .txt thi
cau hinh trong tai lieu se khac cau hinh thuc te trong mo phong. Yeu cau cua de bai la
"nhan subnet, IP va ten thiet bi tren so do phai khop voi cau hinh thuc te".

Packet Tracer luu cau hinh IOS duoi dang van ban trong cac khoi:
  - <RUNNINGCONFIG>  : dang hien thi cua `show running-config` (co dau `!`, mat khau da bam)
  - <STARTUPCONFIG>  : dang phat lai tung lenh khi nap file (co ` exit`, ` no shutdown`)
  - <CONFIG>         : ban sao config.text nam trong flash cua switch
Tat ca deu duoc cap nhat de ba noi khong lech nhau.

Cach dung:  python3 tools/build_variants.py
"""
import hashlib
import os
import re
import sys
import xml.sax.saxutils as su

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pkt_codec  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PKT = os.path.join(ROOT, "CSE3030_2_Nhom6_MinhAn.pkt")
EXT_PKT = os.path.join(ROOT, "CSE3030_2_Nhom6_MinhAn_MoRong_ACL.pkt")

ENABLE_PW = "MinhAn@Enable26"
ADMIN_USER = "admin"
ADMIN_PW = "MinhAn@Admin26"
BANNER = ("banner motd ^C Canh bao: Thiet bi mang Trung tam Dao tao Minh An. "
          "Chi nhan su duoc uy quyen moi duoc truy cap. ^C")

ACL_NAME = "PHONGHOC-IN"
ACL_BODY = [
    "ip access-list extended " + ACL_NAME,
    " remark Khu Phong hoc chi duoc dung DNS/Web va may in cua khu Giao vu",
    " permit udp 172.22.20.0 0.0.0.63 host 172.22.10.5 eq domain",
    " permit tcp 172.22.20.0 0.0.0.63 host 172.22.10.5 eq www",
    " permit ip 172.22.20.0 0.0.0.63 host 172.22.10.6",
    " deny ip 172.22.20.0 0.0.0.63 172.22.10.0 0.0.0.31",
    " permit ip any any",
]
PORT_SECURITY = [
    " switchport port-security",
    " switchport port-security maximum 1",
    " switchport port-security violation restrict",
    " switchport port-security mac-address sticky",
]

I64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def md5crypt(pw: bytes, salt: bytes) -> str:
    """Bam mat khau kieu Cisco type 5 ($1$ / MD5-crypt)."""
    ctx = hashlib.md5(pw + b"$1$" + salt)
    alt = hashlib.md5(pw + salt + pw).digest()
    i = len(pw)
    while i > 0:
        ctx.update(alt[:min(i, 16)])
        i -= 16
    i = len(pw)
    while i:
        ctx.update(b"\x00" if i & 1 else pw[:1])
        i >>= 1
    final = ctx.digest()
    for i in range(1000):
        c = hashlib.md5()
        c.update(pw if i & 1 else final)
        if i % 3:
            c.update(salt)
        if i % 7:
            c.update(pw)
        c.update(final if i & 1 else pw)
        final = c.digest()
    out = ""
    for a, b, c in ((0, 6, 12), (1, 7, 13), (2, 8, 14), (3, 9, 15), (4, 10, 5)):
        v = (final[a] << 16) | (final[b] << 8) | final[c]
        for _ in range(4):
            out += I64[v & 0x3F]
            v >>= 6
    v = final[11]
    for _ in range(2):
        out += I64[v & 0x3F]
        v >>= 6
    return "$1$" + salt.decode() + "$" + out


ENABLE_HASH = md5crypt(ENABLE_PW.encode(), b"mnA1")
ADMIN_HASH = md5crypt(ADMIN_PW.encode(), b"mnA2")


# --------------------------------------------------------------------------
# Truy cap khoi cau hinh ben trong XML
# --------------------------------------------------------------------------

def device_block(xml, name):
    """Tra ve (start, end) cua khoi <DEVICE> chua thiet bi ten `name`."""
    for m in re.finditer(r"<DEVICE>.*?</DEVICE>", xml, re.S):
        if "<NAME translate=\"true\">%s</NAME>" % name in m.group(0):
            return m.start(), m.end()
    raise KeyError("Khong tim thay thiet bi: " + name)


def config_blocks(xml, dev_start, dev_end, tags):
    """Liet ke cac khoi cau hinh trong pham vi mot thiet bi, tu duoi len tren.

    Duyet nguoc de khi thay the khong lam lech chi so cua cac khoi con lai.
    """
    found = []
    for tag in tags:
        for m in re.finditer(r"<%s>(.*?)</%s>" % (tag, tag), xml[dev_start:dev_end], re.S):
            found.append((dev_start + m.start(), dev_start + m.end(), tag, m.group(1)))
    return sorted(found, key=lambda t: -t[0])


def parse_lines(inner):
    """Doc cac phan tu <LINE> thanh danh sach chuoi, kem muc thut le goc."""
    indent = re.search(r"\n(\s*)<LINE>", inner)
    indent = indent.group(1) if indent else "      "
    lines = [su.unescape(m.group(1))
             for m in re.finditer(r"<LINE>(.*?)</LINE>", inner, re.S)]
    return lines, indent


def render_lines(tag, lines, indent):
    body = "".join("\n%s<LINE>%s</LINE>" % (indent, su.escape(l)) for l in lines)
    closing = indent[:-1] if len(indent) >= 1 else ""
    return "<%s>%s\n%s</%s>" % (tag, body, closing, tag)


# --------------------------------------------------------------------------
# Cac phep bien doi tren danh sach dong cau hinh
# --------------------------------------------------------------------------

def _insert_after(lines, predicate, new, once=True):
    out, done = [], False
    for l in lines:
        out.append(l)
        if (not done or not once) and predicate(l):
            out.extend(new)
            done = True
    if not done:
        raise AssertionError("Khong tim thay vi tri chen cho: %r" % (new[:1],))
    return out


def _insert_before(lines, predicate, new, once=True):
    out, done = [], False
    for l in lines:
        if (not done or not once) and predicate(l):
            out.extend(new)
            done = True
        out.append(l)
    if not done:
        raise AssertionError("Khong tim thay vi tri chen truoc cho: %r" % (new[:1],))
    return out


def harden(lines, style, is_router):
    """Them enable secret, tai khoan quan tri, banner va bao ve duong con/vty."""
    if any("enable secret" in l for l in lines):
        return lines  # da va roi

    if style == "run":
        secret_cmds = ["!", "enable secret 5 " + ENABLE_HASH,
                       "!", "username %s privilege 15 secret 5 %s" % (ADMIN_USER, ADMIN_HASH)]
    else:
        secret_cmds = ["enable secret " + ENABLE_PW,
                       "username %s privilege 15 secret %s" % (ADMIN_USER, ADMIN_PW)]

    # 1. Bat ma hoa mat khau hien thi trong cau hinh
    if any(l == "no service password-encryption" for l in lines):
        lines = ["service password-encryption" if l == "no service password-encryption" else l
                 for l in lines]
    else:
        lines = _insert_after(lines, lambda l: l.startswith("version "),
                              ["service password-encryption"])

    # 2. enable secret + tai khoan quan tri, dat ngay sau hostname
    lines = _insert_after(lines, lambda l: l.startswith("hostname "), secret_cmds)

    # 3. Banner canh bao + bao ve duong truy cap
    if style == "run":
        lines = _insert_before(lines, lambda l: l == "line con 0", [BANNER, "!"])
        lines = _insert_after(lines, lambda l: l == "line con 0", [" login local"])
        lines = [" login local" if l == " login" else l for l in lines]
    else:
        if any(l == "line con 0" for l in lines):
            lines = _insert_before(lines, lambda l: l == "line con 0", [BANNER])
            lines = _insert_after(lines, lambda l: l == "line con 0", [" login local"])
            lines = [" login local" if l == " login" else l for l in lines]
        else:
            # Switch: khoi startup chua co line con/vty, phai them truoc `end`
            block = [BANNER,
                     "line con 0", " login local", " exit",
                     "line vty 0 4", " login local", " exit",
                     "line vty 5 15", " login local", " exit"]
            lines = _insert_before(lines, lambda l: l == "end", block)
    return lines


def add_acl(lines, style):
    """Dinh nghia ACL va ap vao cong huong ve khu Phong hoc (G0/1, chieu in).

    ACL phai duoc dinh nghia TRUOC interface tham chieu toi no. Neu dat sau, khi
    Packet Tracer phat lai cau hinh luc nap file, lenh `ip access-group` se tro
    toi mot ACL chua ton tai va co the bi bo qua - phan mo rong khi do im lang
    khong co tac dung, du cau hinh nhin van "co ve" dung.
    """
    if any(ACL_NAME in l for l in lines):
        return lines
    body = ACL_BODY + (["!"] if style == "run" else [" exit"])
    lines = _insert_before(lines, lambda l: l.startswith("interface "), body)

    # Ap ACL vao dung interface GigabitEthernet0/1
    out, inside = [], False
    applied = False
    for l in lines:
        if l.startswith("interface "):
            inside = (l == "interface GigabitEthernet0/1")
        out.append(l)
        if inside and not applied and l.strip().startswith("ip address "):
            out.append(" ip access-group %s in" % ACL_NAME)
            applied = True
    assert applied, "Khong ap duoc ACL vao GigabitEthernet0/1"
    return out


def add_port_security(lines, interfaces):
    """Bat port-security tren cac cong access noi PC (khong ap cho cong noi AP)."""
    if any("port-security" in l for l in lines):
        return lines
    out, cur = [], None
    for l in lines:
        if l.startswith("interface "):
            cur = l[len("interface "):]
        out.append(l)
        if cur in interfaces and l.strip() == "switchport mode access":
            out.extend(PORT_SECURITY)
    assert any("port-security" in l for l in out), "Khong bat duoc port-security"
    return out


# --------------------------------------------------------------------------
# Ap dung len XML
# --------------------------------------------------------------------------

RUN_TAGS = ["RUNNINGCONFIG"]
REPLAY_TAGS = ["STARTUPCONFIG", "CONFIG"]


def patch_device(xml, name, fn_run, fn_replay):
    s, e = device_block(xml, name)
    for bs, be, tag, inner in config_blocks(xml, s, e, RUN_TAGS + REPLAY_TAGS):
        lines, indent = parse_lines(inner)
        if not lines:
            continue
        new = fn_run(lines) if tag in RUN_TAGS else fn_replay(lines)
        xml = xml[:bs] + render_lines(tag, new, indent) + xml[be:]
    return xml


def set_port_acl(xml, dev_name, mac, acl):
    """Gan ACL vao cong co dia chi MAC cho truoc (cong G0/1 cua router)."""
    s, e = device_block(xml, dev_name)
    block = xml[s:e]
    idx = block.find("<MACADDRESS>%s</MACADDRESS>" % mac)
    assert idx != -1, "Khong tim thay cong co MAC " + mac
    start = block.rfind("<PORT>", 0, idx)
    assert start != -1
    seg = block[start:idx]
    assert "<ACL_IN_ID></ACL_IN_ID>" in seg, "Cong nay da co ACL hoac khac cau truc"
    new_seg = seg.replace("<ACL_IN_ID></ACL_IN_ID>",
                          "<ACL_IN_ID>%s</ACL_IN_ID>" % acl, 1)
    block = block[:start] + new_seg + block[idx:]
    return xml[:s] + block + xml[e:]


def export_config(xml, dev_name, path, tag="RUNNINGCONFIG"):
    s, e = device_block(xml, dev_name)
    m = re.search(r"<%s>(.*?)</%s>" % (tag, tag), xml[s:e], re.S)
    lines, _ = parse_lines(m.group(1))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return len(lines)


def main():
    xml = pkt_codec.decode(open(BASE_PKT, "rb").read()).decode("utf-8")
    original = xml

    # ---- Ban co ban: va lo hong bao mat thiet bi -------------------------
    for dev, is_router in (("R-MA", True), ("SW-GIAOVU", False), ("SW-PHONGHOC", False)):
        xml = patch_device(
            xml, dev,
            lambda l, r=is_router: harden(l, "run", r),
            lambda l, r=is_router: harden(l, "start", r),
        )
    if xml == original:
        print("Ban co ban: da duoc va tu truoc, khong co gi de sua")
    base_xml = xml
    open(BASE_PKT, "wb").write(pkt_codec.encode(base_xml.encode("utf-8")))
    print("Da ghi %s" % os.path.basename(BASE_PKT))

    # ---- Ban mo rong: ACL + port-security --------------------------------
    xml = patch_device(base_xml, "R-MA",
                       lambda l: add_acl(l, "run"),
                       lambda l: add_acl(l, "start"))
    xml = set_port_acl(xml, "R-MA", "0212.0000.2002", ACL_NAME)
    pc_ports = {"FastEthernet0/1", "FastEthernet0/2", "FastEthernet0/3"}
    xml = patch_device(xml, "SW-PHONGHOC",
                       lambda l: add_port_security(l, pc_ports),
                       lambda l: add_port_security(l, pc_ports))
    open(EXT_PKT, "wb").write(pkt_codec.encode(xml.encode("utf-8")))
    print("Da ghi %s" % os.path.basename(EXT_PKT))

    # ---- Xuat lai cac ban cau hinh .txt ----------------------------------
    for dev, fname in (("R-MA", "R-MA.txt"), ("SW-GIAOVU", "SW-GIAOVU.txt"),
                       ("SW-PHONGHOC", "SW-PHONGHOC.txt")):
        n = export_config(base_xml, dev, os.path.join(ROOT, fname))
        print("  %-18s %3d dong" % (fname, n))
    for dev, fname in (("R-MA", "R-MA_MoRong_ACL.txt"),
                       ("SW-PHONGHOC", "SW-PHONGHOC_MoRong_PortSecurity.txt")):
        n = export_config(xml, dev, os.path.join(ROOT, fname))
        print("  %-18s %3d dong" % (fname, n))


if __name__ == "__main__":
    main()
