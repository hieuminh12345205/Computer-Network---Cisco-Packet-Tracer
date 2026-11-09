# Bảng kiểm thử

Theo mục 4 của đề bài: mỗi phép thử ghi **nguồn, đích, thao tác, kết quả mong đợi, kết quả
thực tế và minh chứng**. Phép thử nào thất bại thì ghi nguyên nhân và cách xử lý.

**Quy ước:**
- Ô "Kết quả thực tế" có nội dung = **nhóm đã chạy** phép thử trong Packet Tracer 9.0.1 và ghi lại kết quả quan sát được.
- Cột "Minh chứng" có tên ảnh = ảnh nằm trong thư mục [`minh_chung/`](minh_chung/).
- *(cần chụp)* ở cột Minh chứng = đã chạy và đạt, nhưng chưa lưu ảnh.
- *(cần chụp)* ở **cả hai** cột = phép thử đã thiết kế nhưng **chưa chạy**. Không điền sẵn kết quả cho phép thử chưa chạy.

Địa chỉ do DHCP cấp có thể đổi theo thứ tự xin cấp phát khi mở lại file. Trước khi ping một
máy nhận DHCP, luôn đọc IP hiện tại của máy đó bằng `ipconfig`.

---

## A. Phương án cơ bản — `CSE3030_2_Nhom6_MinhAn.pkt`

### A1. Cấp phát DHCP

| # | Nguồn | Đích / thao tác | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|---|
| 1 | PC-GV1 | Desktop > IP Configuration > DHCP | IP trong `172.22.10.10–.29`, mask `255.255.255.224`, GW `172.22.10.1`, DNS `172.22.10.5` | Nhận `172.22.10.12/27`, GW `172.22.10.1`, DNS `172.22.10.5` | [`02_DHCP_PC-GV1`](minh_chung/02_DHCP_PC-GV1.png) |
| 2 | PC-GV2 | Như trên | Cùng dải, **IP khác** PC-GV1 | Nhận `172.22.10.10/27`, khác PC-GV1 | [`03_DHCP_PC-GV2`](minh_chung/03_DHCP_PC-GV2.png) |
| 3 | PC-GV3 | Như trên | Cùng dải, IP không trùng | Nhận `172.22.10.11` (theo bảng binding, phép thử 9) | [`06_R-MA_Route_DHCPBinding`](minh_chung/06_R-MA_Route_DHCPBinding.png) |
| 4 | PC-HV1 | Như trên | IP trong `172.22.20.10–.59`, mask `255.255.255.192`, GW `172.22.20.1`, DNS `172.22.10.5` | Nhận `172.22.20.10/26`, GW `172.22.20.1`, DNS `172.22.10.5` | [`04_DHCP_PC-HV1`](minh_chung/04_DHCP_PC-HV1.png) |
| 5 | PC-HV2 | Như trên | Cùng dải, IP không trùng | Có IP riêng trong dải LAN B (theo bảng binding, phép thử 9) | [`06_R-MA_Route_DHCPBinding`](minh_chung/06_R-MA_Route_DHCPBinding.png) |
| 6 | PC-HV3 | Như trên | Cùng dải, IP không trùng | Nhận `172.22.20.10/26` ở lần mở file sau, khác lần trước → địa chỉ DHCP có thể đổi giữa các lần mở | [`05_DHCP_PC-HV3`](minh_chung/05_DHCP_PC-HV3.png) |
| 7 | LT-GV1 | Như trên (qua Wi-Fi) | IP dải LAN B, DNS `172.22.10.5` | Nhận `172.22.20.12`, DNS `172.22.10.5`, qua SSID `MINHAN-TEACHER` | [`12_Wifi_LT-GV1_ThongTin`](minh_chung/12_Wifi_LT-GV1_ThongTin.png) |
| 8 | LT-GV2 | Như trên (qua Wi-Fi) | IP dải LAN B, IP khác LT-GV1 | Có IP riêng trong dải LAN B, khác LT-GV1 (theo bảng binding) | [`06_R-MA_Route_DHCPBinding`](minh_chung/06_R-MA_Route_DHCPBinding.png) |
| 9 | R-MA (CLI) | `show ip dhcp binding` | Liệt kê đủ 8 máy, **không có IP trùng nhau** | 8 dòng: 3 IP `172.22.10.10–.12` và 5 IP `172.22.20.10–.14`, **không trùng** | [`06_R-MA_Route_DHCPBinding`](minh_chung/06_R-MA_Route_DHCPBinding.png) |
| 10 | R-MA (CLI) | `show ip dhcp pool` | Hai pool `GIAOVU`, `PHONGHOC`; số địa chỉ đã cấp khớp số máy | `GIAOVU`: 3 leased / 30; `PHONGHOC`: 5 leased / 62 → khớp 3 PC LAN A và 3 PC + 2 laptop LAN B | [`28_R-MA_DHCPPool`](minh_chung/28_R-MA_DHCPPool.png) |

> Phép thử 9 là cách gọn nhất để chứng minh "không trùng IP" mà đề bài yêu cầu, thay vì mở
> lần lượt từng máy.

### A2. Kết nối trong cùng một LAN

| # | Nguồn | Đích / thao tác | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|---|
| 11 | PC-GV1 | `ping 172.22.10.1` (gateway LAN A) | 4/4 phản hồi | 4/4, TTL=255 (router) | [`25_Ping_PC-GV1_Gateway_PC-GV2`](minh_chung/25_Ping_PC-GV1_Gateway_PC-GV2.png) |
| 12 | PC-GV1 | `ping` tới IP hiện tại của PC-GV2 | 4/4 phản hồi (gói đầu có thể mất do ARP) | PC-GV2 lần này là `172.22.10.11`: 4/4, TTL=128 | [`25_Ping_PC-GV1_Gateway_PC-GV2`](minh_chung/25_Ping_PC-GV1_Gateway_PC-GV2.png) |
| 13 | PC-HV1 | `ping 172.22.20.1` (gateway LAN B) | 4/4 phản hồi | 4/4, TTL=255 | [`26_Ping_PC-HV1_Gateway_PC-HV2_MayChu`](minh_chung/26_Ping_PC-HV1_Gateway_PC-HV2_MayChu.png) |
| 14 | PC-HV1 | `ping` tới IP hiện tại của PC-HV2 | 4/4 phản hồi | PC-HV2 `172.22.20.10`: 4/4, TTL=128 | [`26_Ping_PC-HV1_Gateway_PC-HV2_MayChu`](minh_chung/26_Ping_PC-HV1_Gateway_PC-HV2_MayChu.png) |

### A3. Kết nối giữa hai LAN

| # | Nguồn | Đích / thao tác | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|---|
| 15 | PC-HV1 | Simple PDU tới SRV-PORTAL | Successful | Successful | [`17_Simulation_PC-GV1_PC-HV3`](minh_chung/17_Simulation_PC-GV1_PC-HV3.png) |
| 16 | PC-GV1 | Simple PDU tới PC-HV3 | Successful | Successful; Event List đi qua SW-GIAOVU → R-MA → SW-PHONGHOC → **PC-HV3** và quay về | [`17_Simulation_PC-GV1_PC-HV3`](minh_chung/17_Simulation_PC-GV1_PC-HV3.png) |
| 17 | PC-HV1 | `ping 172.22.10.5` | 4/4 phản hồi | Lần 1: 3/4 (gói đầu mất do ARP); lần 2: 4/4. TTL=127 (qua 1 router) | [`26_Ping_PC-HV1_Gateway_PC-HV2_MayChu`](minh_chung/26_Ping_PC-HV1_Gateway_PC-HV2_MayChu.png) |
| 18 | PC-HV1 | `tracert 172.22.10.5` | Hiện **2 chặng**: `172.22.20.1` rồi `172.22.10.5` | 2 chặng: `172.22.20.1` → `172.22.10.5`, "Trace complete" | [`27_Tracert_NSLookup_PC-HV1`](minh_chung/27_Tracert_NSLookup_PC-HV1.png) |
| 19 | R-MA (CLI) | `show ip route` | Hai dòng `C` cho `172.22.10.0/27` và `172.22.20.0/26` | 2 dòng `C` đúng như mong đợi, thêm 2 dòng `L` (địa chỉ của chính router) | [`06_R-MA_Route_DHCPBinding`](minh_chung/06_R-MA_Route_DHCPBinding.png) |
| 20 | R-MA (CLI) | `show ip interface brief` | `G0/0` và `G0/1` đều `up/up`; `G0/2` administratively down | G0/0, G0/1 `up/up`; G0/2 administratively down | [`07_R-MA_InterfaceBrief`](minh_chung/07_R-MA_InterfaceBrief.png) |

> **Nguyên nhân phép thử 16 thất bại ở lần gửi đầu:** khi mạng vừa khởi động hoặc vừa đổi
> cấu hình Wi-Fi, ARP và DHCP chưa hoàn tất nên Simple PDU đầu tiên báo Failed.
> **Cách xử lý:** bấm Fast Forward Time cho mạng hội tụ rồi gửi lại. Không kết luận lỗi định
> tuyến chỉ từ một Simple PDU đầu tiên.

### A4. DNS và website nội bộ

| # | Nguồn | Đích / thao tác | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|---|
| 21 | PC-GV1 | Web Browser → `http://portal.minhan.test` | Hiện trang cổng thông tin | Đạt | [`08_Web_PC-GV1_TenMien`](minh_chung/08_Web_PC-GV1_TenMien.png) |
| 22 | PC-HV1 | Như trên | Hiện đúng trang đó (đi xuyên router) | Đạt | [`10_Web_PC-HV1`](minh_chung/10_Web_PC-HV1.png) |
| 23 | PC-GV1 | `http://172.22.10.5` | Cùng một trang → tách được lỗi DNS khỏi lỗi HTTP | Đạt (chạy trên PC-GV1): cùng một trang | [`09_Web_PC-GV1_IP`](minh_chung/09_Web_PC-GV1_IP.png) |
| 24 | PC-HV1 | `nslookup portal.minhan.test` | Trả về `172.22.10.5` | Server `172.22.10.5`, trả lời `portal.minhan.test` → `172.22.10.5` | [`27_Tracert_NSLookup_PC-HV1`](minh_chung/27_Tracert_NSLookup_PC-HV1.png) |

### A5. Wi-Fi và máy in

| # | Nguồn | Đích / thao tác | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|---|
| 25 | LT-GV1 | Desktop > PC Wireless | Đã nối SSID `MINHAN-TEACHER`, bảo mật WPA2-PSK | LT-GV1: "successfully connected", SSID `MINHAN-TEACHER`, Security WPA2-Personal | [`11_Wifi_LT-GV1_KetNoi`](minh_chung/11_Wifi_LT-GV1_KetNoi.png), [`12_Wifi_LT-GV1_ThongTin`](minh_chung/12_Wifi_LT-GV1_ThongTin.png) |
| 26 | LT-GV1 | `http://portal.minhan.test` | Mở được trang qua sóng Wi-Fi | Đạt (chạy trên LT-GV1) | [`13_Web_Wifi_LT-GV1`](minh_chung/13_Web_Wifi_LT-GV1.png) |
| 27 | LT-GV2 | `ping 172.22.10.6` (máy in) | 4/4 phản hồi | 4/4, mất 0%, TTL=127, thời gian 12–32 ms (Wi-Fi chậm hơn dây) | [`16_MayIn_LT-GV2_Wifi`](minh_chung/16_MayIn_LT-GV2_Wifi.png) |
| 28 | PC-GV1 | `ping 172.22.10.6` | 4/4 phản hồi (máy in cùng LAN) | 4/4, TTL=128 (cùng LAN, không qua router) | [`14_MayIn_PC-GV1`](minh_chung/14_MayIn_PC-GV1.png) |

| 28b | PC-HV1 | `ping 172.22.10.6` | 4/4 phản hồi (khác LAN, qua router) | 4/4, TTL=127 | [`15_MayIn_PC-HV1`](minh_chung/15_MayIn_PC-HV1.png) |

> Đề bài ghi rõ: **không yêu cầu mô phỏng in tài liệu thực tế**, chỉ cần chứng minh máy in
> có IP phù hợp và liên lạc được.

### A6. Quan sát gói tin

| # | Nguồn | Đích / thao tác | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|---|
| 29 | PC-GV1 | Simulation, lọc ICMP+ARP, Simple PDU tới PC-HV3 | Đường đi `PC-GV1 → SW-GIAOVU → R-MA → SW-PHONGHOC → PC-HV3`, phản hồi ngược lại | Successful; đường đi đúng | [`17_Simulation_PC-GV1_PC-HV3`](minh_chung/17_Simulation_PC-GV1_PC-HV3.png) |
| 30 | PC-HV1 | Simulation, lọc thêm DNS+HTTP, mở trang web | Thứ tự **DNS query → DNS response → TCP SYN/SYN-ACK/ACK → HTTP** | *(cần chụp)* | |

### A7. Lưu cấu hình và nạp lại

| # | Nguồn | Đích / thao tác | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|---|
| 31 | LT-GV1 | Mở lại file, chờ hội tụ, mở portal | Dịch vụ hoạt động lại bình thường | Đạt | `08_MoLaiFile_Web_LT1.png` |
| 32 | R-MA (CLI) | `show running-config` so với `show startup-config` | Hai bản giống nhau → đã `copy running-config startup-config` | *(cần chụp)* | |

### A8. Bảo vệ truy cập thiết bị

| # | Nguồn | Đích / thao tác | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|---|
| 33 | R-MA | Mở tab CLI | Hiện banner cảnh báo, hỏi username/password | Hiện banner `Canh bao: ...`, hỏi Username/Password | [`18_R-MA_DangNhap`](minh_chung/18_R-MA_DangNhap.png) |
| 34 | R-MA | Đăng nhập `admin` / `MinhAn@Admin26` | Vào thẳng chế độ privileged `R-MA#` (tài khoản privilege 15); `enable` không hỏi thêm mật khẩu | Vào thẳng `R-MA#`; `enable` không hỏi thêm | [`18_R-MA_DangNhap`](minh_chung/18_R-MA_DangNhap.png) |
| 35 | PC-GV1 | `telnet 172.22.10.2` (quản trị SW-GIAOVU) | Hỏi đăng nhập và vào được bằng tài khoản trên | Kết nối "Open", hiện banner, đăng nhập `admin` vào `SW-GIAOVU>` | [`29_Telnet_PC-GV1_SW-GIAOVU`](minh_chung/29_Telnet_PC-GV1_SW-GIAOVU.png) |

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
