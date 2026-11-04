# tools/ — công cụ đọc và sửa file Packet Tracer

Thư mục này không phải sản phẩm nộp. Nó chỉ phục vụ việc **kiểm tra và sửa cấu hình bên
trong file `.pkt`** một cách có thể lặp lại, thay vì sửa tay rồi quên không đồng bộ sang
các bản xuất `.txt`.

| File | Vai trò |
|---|---|
| `pkt_codec.py` | Giải mã / mã hoá file `.pkt` (Packet Tracer 8.x–9.x) |
| `build_variants.py` | Dựng bản cơ bản (đã vá bảo mật) và bản mở rộng (ACL + port-security) |
| `libtwofish.so` | Thư viện Twofish dùng chung, biên dịch sẵn cho Linux x86-64 |

## Định dạng file .pkt

File `.pkt` là XML đã qua bốn lớp xử lý. Khi **giải mã** thì đi theo thứ tự:

1. **Khử xáo trộn ngoài:** `b[i] = a[L-1-i] ^ ((L * (1 - i)) & 0xFF)`, với `L` là độ dài file.
2. **Giải mã:** **Twofish** chế độ **EAX**, key = 16 byte `0x89`, IV = 16 byte `0x10`,
   thẻ xác thực 16 byte nằm ở cuối bản mã.
3. **Khử xáo trộn trong:** `b[i] = a[i] ^ ((L - i) & 0xFF)`.
4. **Giải nén:** 4 byte đầu (big-endian) là kích thước sau giải nén, phần còn lại là zlib.

Khi **mã hoá** thì làm ngược lại, thứ tự 4 → 1. Lưu ý lớp 1 **không** phải phép biến đổi tự
nghịch đảo: khi đảo chiều, mặt nạ `(L * (1 - i))` phải đổi thành `(L * (2 - L + i))`.
Nén bằng zlib **mức 6** để khớp đúng byte với bản do Packet Tracer tự ghi ra.

## Kiểm chứng

```bash
python3 tools/pkt_codec.py selftest CSE3030_MinhAn.pkt
```

Lệnh này giải mã rồi mã hoá lại và so sánh. Với file gốc do Packet Tracer ghi, kết quả mã
hoá lại **trùng từng byte** với file gốc — đó là bằng chứng bộ codec tái tạo đúng định dạng,
không phải chỉ "đọc tạm được".

## Dựng lại hai bản mô phỏng

```bash
python3 tools/build_variants.py
```

Script sửa cấu hình IOS ngay trong XML, ở **tất cả** các khối lưu cấu hình, nên ba nơi không
bị lệch nhau:

- `<RUNNINGCONFIG>` — dạng hiển thị của `show running-config` (mật khẩu đã băm type 5)
- `<STARTUPCONFIG>` — dạng phát lại từng lệnh khi Packet Tracer nạp file
- `<CONFIG>` — bản sao `config.text` trong flash của switch

Script có tính idempotent: chạy lại nhiều lần không nhân đôi cấu hình.

> **Lưu ý về thứ tự lệnh:** trong khối phát lại, ACL **phải** được định nghĩa trước
> interface tham chiếu tới nó. Nếu đặt sau, lệnh `ip access-group` sẽ trỏ tới một ACL chưa
> tồn tại và có thể bị bỏ qua lúc nạp file — phần mở rộng khi đó im lặng không có tác dụng
> dù cấu hình nhìn vẫn "có vẻ" đúng.

## Biên dịch lại libtwofish.so

Dùng mã nguồn Twofish của Niels Ferguson (gói PyPI `twofish`, file `twofish-0.3/twofish.c`):

```bash
pip download twofish --no-binary :all: --no-deps -d /tmp/tf && tar xzf /tmp/tf/*.tar.gz -C /tmp/tf
```

```bash
gcc -O2 -shared -fPIC -o tools/libtwofish.so /tmp/tf/twofish-0.3.0/twofish-0.3/twofish.c
```

Phần CMAC/OMAC và chế độ EAX được cài trong `pkt_codec.py`, đã đối chiếu với vector thử
chuẩn của MD5-crypt và với hash type 5 đã biết của mật khẩu `cisco`
(`$1$mERr$hx5rVt7rPNoS4wqbXKX7m0`).
