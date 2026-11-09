# Bảng kiểm thử

Theo mục 4 của đề bài: mỗi phép thử ghi **nguồn, đích, thao tác, kết quả mong đợi, kết quả
thực tế và minh chứng**. Phép thử nào thất bại thì ghi nguyên nhân và cách xử lý.

**Quy ước cột "Kết quả thực tế":**
- Ô có mô tả kết quả và tên file ảnh = **đã chạy và đã có minh chứng**.
- Ô ghi *(cần chụp)* = phép thử đã được thiết kế, nêu rõ kết quả mong đợi, **nhóm cần tự
  chạy và chụp màn hình** trước khi nộp. Không điền sẵn kết quả cho những phép thử chưa chạy.

Địa chỉ do DHCP cấp có thể đổi theo thứ tự xin cấp phát khi mở lại file. Trước khi ping một
máy nhận DHCP, luôn đọc IP hiện tại của máy đó bằng `ipconfig`.

---

## A. Phương án cơ bản — `CSE3030_2_Nhom6_MinhAn.pkt`

### A1. Cấp phát DHCP

| # | Nguồn | Đích / thao tác | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|---|
| 1 | PC-GV1 | Desktop > IP Configuration > DHCP | IP trong `172.22.10.10–.29`, mask `255.255.255.224`, GW `172.22.10.1`, DNS `172.22.10.5` | Nhận `172.22.10.11/27`, GW và DNS đúng | — |
| 2 | PC-GV2 | Như trên | Cùng dải, **IP khác** PC-GV1 | *(cần chụp)* | |
| 3 | PC-GV3 | Như trên | Cùng dải, IP không trùng | *(cần chụp)* | |
| 4 | PC-HV1 | Như trên | IP trong `172.22.20.10–.59`, mask `255.255.255.192`, GW `172.22.20.1`, DNS `172.22.10.5` | Nhận đúng dải LAN B | `05_DHCP_LAN_B.png` |
| 5 | PC-HV2 | Như trên | Cùng dải, IP không trùng | *(cần chụp)* | |
| 6 | PC-HV3 | Như trên | Cùng dải, IP không trùng | *(cần chụp)* | |
| 7 | LT-GV1 | Như trên (qua Wi-Fi) | IP dải LAN B, DNS `172.22.10.5` | Nhận `172.22.20.14` | — |
| 8 | LT-GV2 | Như trên (qua Wi-Fi) | IP dải LAN B, IP khác LT-GV1 | Nhận `172.22.20.13` | — |
| 9 | R-MA (CLI) | `show ip dhcp binding` | Liệt kê đủ 8 máy, **không có IP trùng nhau** | *(cần chụp)* | |
| 10 | R-MA (CLI) | `show ip dhcp pool` | Hai pool `GIAOVU`, `PHONGHOC`; số địa chỉ đã cấp khớp số máy | *(cần chụp)* | |

> Phép thử 9 là cách gọn nhất để chứng minh "không trùng IP" mà đề bài yêu cầu, thay vì mở
> lần lượt từng máy.

### A2. Kết nối trong cùng một LAN

| # | Nguồn | Đích / thao tác | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|---|
| 11 | PC-GV1 | `ping 172.22.10.1` (gateway LAN A) | 4/4 phản hồi | *(cần chụp)* | |
| 12 | PC-GV1 | `ping` tới IP hiện tại của PC-GV2 | 4/4 phản hồi (gói đầu có thể mất do ARP) | *(cần chụp)* | |
| 13 | PC-HV1 | `ping 172.22.20.1` (gateway LAN B) | 4/4 phản hồi | *(cần chụp)* | |
| 14 | PC-HV1 | `ping` tới IP hiện tại của PC-HV2 | 4/4 phản hồi | *(cần chụp)* | |

### A3. Kết nối giữa hai LAN

| # | Nguồn | Đích / thao tác | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|---|
| 15 | PC-HV1 | Simple PDU tới SRV-PORTAL | Successful | Successful | — |
| 16 | PC-GV1 | Simple PDU tới PC-HV3 | Successful | Successful sau khi gửi lại lần hai | `04_KetNoi_HaiLAN.png` |
| 17 | PC-HV1 | `ping 172.22.10.5` | 4/4 phản hồi | *(cần chụp)* | |
| 18 | PC-HV1 | `tracert 172.22.10.5` | Hiện **2 chặng**: `172.22.20.1` rồi `172.22.10.5` | *(cần chụp)* | |
| 19 | R-MA (CLI) | `show ip route` | Hai dòng `C` cho `172.22.10.0/27` và `172.22.20.0/26` | *(cần chụp)* | |
| 20 | R-MA (CLI) | `show ip interface brief` | `G0/0` và `G0/1` đều `up/up`; `G0/2` administratively down | *(cần chụp)* | |

> **Nguyên nhân phép thử 16 thất bại ở lần gửi đầu:** khi mạng vừa khởi động hoặc vừa đổi
> cấu hình Wi-Fi, ARP và DHCP chưa hoàn tất nên Simple PDU đầu tiên báo Failed.
> **Cách xử lý:** bấm Fast Forward Time cho mạng hội tụ rồi gửi lại. Không kết luận lỗi định
> tuyến chỉ từ một Simple PDU đầu tiên.

### A4. DNS và website nội bộ

| # | Nguồn | Đích / thao tác | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|---|
| 21 | PC-GV1 | Web Browser → `http://portal.minhan.test` | Hiện trang cổng thông tin | Đạt | `01_Web_LAN_A.png` |
| 22 | PC-HV1 | Như trên | Hiện đúng trang đó (đi xuyên router) | Đạt | `06_Web_PC_LAN_B.png` |
| 23 | PC-HV1 | `http://172.22.10.5` | Cùng một trang → tách được lỗi DNS khỏi lỗi HTTP | *(cần chụp)* | |
| 24 | PC-HV1 | `nslookup portal.minhan.test` | Trả về `172.22.10.5` | *(cần chụp)* | |

### A5. Wi-Fi và máy in

| # | Nguồn | Đích / thao tác | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|---|
| 25 | LT-GV2 | Desktop > PC Wireless | Đã nối SSID `MINHAN-TEACHER`, bảo mật WPA2-PSK | *(cần chụp)* | |
| 26 | LT-GV2 | `http://portal.minhan.test` | Mở được trang qua sóng Wi-Fi | Đạt | `03_Web_Wifi_LAN_B.png` |
| 27 | LT-GV2 | `ping 172.22.10.6` (máy in) | 4/4 phản hồi | 4/4, mất gói 0% | `02_Wifi_Ping_MayIn.png` |
| 28 | PC-GV1 | `ping 172.22.10.6` | 4/4 phản hồi (máy in cùng LAN) | *(cần chụp)* | |

> Đề bài ghi rõ: **không yêu cầu mô phỏng in tài liệu thực tế**, chỉ cần chứng minh máy in
> có IP phù hợp và liên lạc được.

### A6. Quan sát gói tin

| # | Nguồn | Đích / thao tác | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|---|
| 29 | PC-GV1 | Simulation, lọc ICMP+ARP, Simple PDU tới PC-HV3 | Đường đi `PC-GV1 → SW-GIAOVU → R-MA → SW-PHONGHOC → PC-HV3`, phản hồi ngược lại | Cả 4 PDU Successful | `07_Simulation_ICMP.png` |
| 30 | PC-HV1 | Simulation, lọc thêm DNS+HTTP, mở trang web | Thứ tự **DNS query → DNS response → TCP SYN/SYN-ACK/ACK → HTTP** | *(cần chụp)* | |

### A7. Lưu cấu hình và nạp lại

| # | Nguồn | Đích / thao tác | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|---|
| 31 | LT-GV1 | Mở lại file, chờ hội tụ, mở portal | Dịch vụ hoạt động lại bình thường | Đạt | `08_MoLaiFile_Web_LT1.png` |
| 32 | R-MA (CLI) | `show running-config` so với `show startup-config` | Hai bản giống nhau → đã `copy running-config startup-config` | *(cần chụp)* | |

### A8. Bảo vệ truy cập thiết bị

| # | Nguồn | Đích / thao tác | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|---|
| 33 | R-MA | Mở tab CLI | Hiện banner cảnh báo, hỏi username/password | *(cần chụp)* | |
| 34 | R-MA | Đăng nhập `admin` / `MinhAn@Admin26` | Vào thẳng chế độ privileged `R-MA#` (tài khoản privilege 15); `enable` không hỏi thêm mật khẩu | *(cần chụp)* | |
| 35 | PC-GV1 | `telnet 172.22.10.2` (quản trị SW-GIAOVU) | Hỏi đăng nhập và vào được bằng tài khoản trên | *(cần chụp)* | |

> Trước khi vá, cả ba thiết bị đều đặt `login` trên đường VTY **nhưng không có mật khẩu**,
> nên mọi phiên telnet đều bị từ chối với thông báo *"Password required, but none set"*.
> Phép thử 35 chính là phép thử hồi quy cho lỗi đó.

---

## B. Phần mở rộng — `CSE3030_2_Nhom6_MinhAn_MoRong_ACL.pkt`

Xem bảng E1–E8 trong [`MO_RONG_ACL.md`](MO_RONG_ACL.md#5-bảng-kiểm-thử-phần-mở-rộng),
gồm cả trường hợp **được phép** và trường hợp **bị chặn** như đề bài yêu cầu.

---

## C. Những hạn chế còn lại

- Các phép thử trên là phép thử **đại diện**, không phải đã thử mọi cặp thiết bị trong mạng.
- Chưa có kết nối Internet thật, chưa có NAT, chưa mô phỏng in tài liệu thực tế.
- Chưa kiểm tra khả năng mở file trên phiên bản Packet Tracer cũ hơn 9.0.1.
- Phương án hiện tại ở **một địa điểm**, chưa có dự phòng đường truyền hay thiết bị.
