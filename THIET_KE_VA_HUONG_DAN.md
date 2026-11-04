# Thiết kế mạng trung tâm đào tạo Minh An

**File chính:** `CSE3030_MinhAn.pkt`  
**Phiên bản đã dùng để mở và kiểm tra:** Cisco Packet Tracer 9.0.1.0858  
**Ngày thực hiện:** 04/11/2026

## 1. Ý tưởng và phạm vi

Trung tâm Minh An có khoảng 30 người dùng: 8 nhân sự Giáo vụ và 22 người dùng tại khu Phòng học, gồm học viên và giảng viên. Giáo vụ quản lý hồ sơ, lịch học và thông báo. Phòng học truy cập tài liệu trên cổng thông tin nội bộ. Giảng viên dùng laptop kết nối Wi-Fi; hai khu dùng chung một máy in.

Đây là thiết kế mới, với tên đơn vị, sơ đồ bố trí, địa chỉ IP, SSID và nội dung website riêng. File `GK.pkt` chỉ được mở để tham khảo; không được dùng làm dữ liệu đầu vào cho mã dựng mô hình.

Mô hình hoàn thành phần cơ bản: hai subnet nối trực tiếp vào một router, DHCP trên router, DNS và HTTP trên server, Wi-Fi WPA2-PSK/AES, máy in IP tĩnh. Phạm vi chưa gồm Internet, NAT, ACL, dự phòng hay định tuyến động. Việc chia subnet tạo hai miền quảng bá; bản thân nó không chặn truy cập giữa hai khu.

## 2. Sơ đồ và danh mục thiết bị

```text
                           R-MA (2911)
                    G0/0             G0/1
                      |                |
                SW-GIAOVU         SW-PHONGHOC
                 (2960)             (2960)
                 /  |  \             /    \
              3 PC Server Máy in   3 PC     AP-GIANGVIEN
                                              )) 2 laptop
```

| Thiết bị | Số lượng | Tên trên mô hình / vai trò |
|---|---:|---|
| Router 2911 | 1 | R-MA: gateway hai LAN, định tuyến và DHCP |
| Switch 2960-24TT | 2 | SW-GIAOVU, SW-PHONGHOC: kết nối lớp 2 |
| PC-PT | 6 | PC-GV1..3, PC-HV1..3: máy trạm đại diện |
| Server-PT | 1 | SRV-PORTAL: DNS + HTTP |
| Printer-PT | 1 | PRN-GIAOVU: máy in dùng chung |
| AccessPoint-PT | 1 | AP-GIANGVIEN: cầu nối Wi-Fi vào LAN B |
| Laptop-PT + WPC300N | 2 | LT-GV1, LT-GV2: laptop giảng viên |

Tổng cộng **14 thiết bị mạng và đầu cuối trên Logical**. Thành phần cấp điện tự sinh trong Physical Workspace, nếu xuất hiện, không phải một khu mạng bổ sung. Các PC và laptop là thiết bị đại diện, không phải toàn bộ 30 người dùng thực tế.

### Bảng nối cổng

| Đầu A | Đầu B | Loại kết nối |
|---|---|---|
| R-MA G0/0 | SW-GIAOVU G0/1 | Copper straight-through |
| R-MA G0/1 | SW-PHONGHOC G0/1 | Copper straight-through |
| SW-GIAOVU F0/1..3 | PC-GV1..3 F0 | Copper straight-through |
| SW-GIAOVU F0/4 | SRV-PORTAL F0 | Copper straight-through |
| SW-GIAOVU F0/5 | PRN-GIAOVU F0 | Copper straight-through |
| SW-PHONGHOC F0/1..3 | PC-HV1..3 F0 | Copper straight-through |
| SW-PHONGHOC F0/4 | AP-GIANGVIEN Port 0 | Copper straight-through |
| AP-GIANGVIEN Port 1 | LT-GV1, LT-GV2 Wireless0 | Wi-Fi |

## 3. Kế hoạch địa chỉ IPv4

| Thuộc tính | LAN A - Giáo vụ | LAN B - Phòng học |
|---|---|---|
| Mạng | 172.22.10.0/27 | 172.22.20.0/26 |
| Subnet mask | 255.255.255.224 | 255.255.255.192 |
| Host dùng được | 172.22.10.1 - 172.22.10.30 | 172.22.20.1 - 172.22.20.62 |
| Broadcast | 172.22.10.31 | 172.22.20.63 |
| Default gateway | 172.22.10.1 | 172.22.20.1 |
| IP quản trị switch | 172.22.10.2 | 172.22.20.2 |
| Dải DHCP | 172.22.10.10 - 172.22.10.29 | 172.22.20.10 - 172.22.20.59 |
| DNS cấp qua DHCP | 172.22.10.5 | 172.22.10.5 |

**IP tĩnh:** SRV-PORTAL = `172.22.10.5/27`; PRN-GIAOVU = `172.22.10.6/27`. Cả hai dùng gateway `172.22.10.1`. AP trong mô hình này hoạt động như cầu nối lớp 2 và không có trang cấu hình IP quản trị; không cần gán một IP giả cho AP.

Chọn dải private 172.22.x.x để tách biệt với ví dụ của đề. /27 cung cấp 30 địa chỉ host cho khu Giáo vụ nhỏ; /26 cung cấp 62 địa chỉ host cho Phòng học lớn hơn. Dải DHCP chừa chỗ cho hạ tầng tĩnh và mở rộng; không cấp địa chỉ mạng hoặc broadcast.

Địa chỉ DHCP cụ thể có thể thay đổi theo thứ tự xin cấp phát khi mở lại file. Trong lần kiểm thử, PC-GV1 nhận `172.22.10.11`, PC-HV1 nhận `172.22.20.12`, LT-GV1 nhận `172.22.20.14`, LT-GV2 nhận `172.22.20.13`. Không dùng các số cuối này làm cấu hình cố định.

## 4. Dịch vụ đã cấu hình

- Router có hai pool `GIAOVU` và `PHONGHOC`; loại trừ `.1-.9` và `.30` ở LAN A, `.1-.9` và `.60-.62` ở LAN B. Các cổng G0/0, G0/1 đã bật. Hai mạng được định tuyến trực tiếp.
- DNS trên SRV-PORTAL có bản ghi A `portal.minhan.test` trỏ tới `172.22.10.5`.
- HTTP bật trên server. Trang chủ được viết riêng cho trung tâm, có lịch học và thông tin dịch vụ dùng chung.
- Wi-Fi: SSID **MINHAN-TEACHER**, **WPA2-PSK**, **AES**. Khóa thử nghiệm: **MinhAnLab2026!** (có dấu `!` cuối). Hai laptop đã lắp card WPC300N và dùng DHCP.
- Hai switch dùng VLAN 1 trong phương án cơ bản; mỗi LAN được tách bởi một cổng router. Chưa triển khai VLAN theo phòng ban trên một đường trunk.
- Các file `R-MA.txt`, `SW-GIAOVU.txt`, `SW-PHONGHOC.txt` chứa cấu hình IOS xuất từ bản mô phỏng đã lưu.

## 5. Kết quả kiểm thử đại diện

| Nguồn | Đích / thao tác | Mong đợi | Kết quả thực tế / minh chứng |
|---|---|---|---|
| PC-GV1 | Desktop > IP Configuration | DHCP đúng LAN A, gateway, DNS | 172.22.10.11/27; gateway .1; DNS 172.22.10.5 |
| PC-HV1 | Desktop > IP Configuration | DHCP đúng LAN B, gateway, DNS | Đạt; ảnh `05_DHCP_LAN_B.png` |
| PC-GV1 | http://portal.minhan.test | Phân giải DNS và tải web | Đạt; ảnh `01_Web_LAN_A.png` |
| PC-HV1 | http://portal.minhan.test | Web qua router từ PC LAN B | Đạt; ảnh `06_Web_PC_LAN_B.png` |
| LT-GV2 | http://portal.minhan.test | Web qua Wi-Fi WPA2 từ LAN B | Đạt; ảnh `03_Web_Wifi_LAN_B.png` |
| PC-HV1 | Simple PDU tới SRV-PORTAL | ICMP giữa hai LAN | Successful |
| PC-GV1 | Simple PDU tới PC-HV3 | ICMP chiều LAN A sang LAN B | Successful sau khi gửi lại; ảnh `04_KetNoi_HaiLAN.png` |
| LT-GV2 | ping 172.22.10.6 | Liên lạc máy in qua Wi-Fi và router | 4/4 phản hồi, 0% mất gói; ảnh `02_Wifi_Ping_MayIn.png` |
| Các PDU đã tạo | Chạy lại trong Simulation Mode | Quan sát truyền gói qua switch/router/AP | Cả 4 PDU báo Successful; ảnh `07_Simulation_ICMP.png` |
| LT-GV1 | Mở lại file cuối, chờ mạng lên, truy cập portal | Cấu hình và dịch vụ hoạt động sau khi nạp lại | Đạt; ảnh `08_MoLaiFile_Web_LT1.png` |

Một số Simple PDU đầu tiên đã báo Failed trước khi gửi lại. Các gói gửi lại và phép ping bốn gói đã thành công. Khi mạng vừa khởi động hoặc mới đổi bảo mật Wi-Fi, cần chờ kết nối, DHCP và quá trình ARP hoàn tất rồi thử lại; không kết luận lỗi định tuyến chỉ từ một Simple PDU đầu tiên. Lịch sử thử được giữ để đối chiếu.

Các kết quả trên là phép thử đại diện đã thực hiện, không phải khẳng định đã thử mọi cặp thiết bị. Khi nhóm chuẩn bị báo cáo, bổ sung ping giữa hai PC cùng LAN, ping gateway ở mỗi LAN và kiểm tra IP của đủ 6 PC, 2 laptop.

## 6. Cách mở và trình bày

1. Mở `CSE3030_MinhAn.pkt` bằng Packet Tracer 9.0.1. Chọn Logical và Realtime. Nếu máy dùng cửa sổ nhỏ, phóng to cửa sổ hoặc Zoom Out để thấy đủ hai khu.
2. Chờ các liên kết lên và DHCP hoàn tất. Có thể dùng nút Fast Forward Time. Mở PC > Desktop > IP Configuration để xem IP, mask, gateway và DNS.
3. Mở Desktop > Web Browser, nhập **http://portal.minhan.test**. Đây là tên miền trong mô hình; mở bằng trình duyệt bên ngoài Packet Tracer sẽ không truy cập server mô phỏng.
4. Dùng Command Prompt bên trong PC/laptop để chạy `ping 172.22.10.6`, hoặc gửi Simple PDU giữa hai thiết bị. Khi cần ping một PC nhận DHCP, đọc IP hiện tại của máy đó trước.
5. Quan sát gói tin: chuyển Simulation, giữ ICMP/ARP trong Edit Filters, tạo Simple PDU, dùng Capture/Forward từng bước. Tuyến PC-GV1 tới PC-HV3 là **PC-GV1 > SW-GIAOVU > R-MA > SW-PHONGHOC > PC-HV3**, phản hồi đi ngược lại. Switch chuyển tiếp khung Ethernet; router xử lý việc chuyển gói giữa hai subnet. Khi chưa biết MAC của gateway hoặc máy đích, ARP diễn ra trước ICMP.
6. Với web, giải thích thứ tự **DNS > thiết lập TCP > HTTP**. IP DNS thuộc LAN A nên client LAN B cần gateway để hỏi DNS.
7. Sau khi thay đổi cấu hình IOS bằng CLI, dùng `copy running-config startup-config` trên thiết bị rồi lưu file Packet Tracer bằng Ctrl+S.

## 7. Việc nhóm cần bổ sung trước khi nộp

Điền đúng mã lớp, số nhóm, tên thành viên và phân công thực tế. Đổi tên file theo quy tắc của lớp nếu cần. Xác nhận phiên bản Packet Tracer giảng viên dùng; bản này đã kiểm tra trên 9.0.1, chưa xác nhận mở được trên bản cũ hơn. Đây là phương án cơ bản tại một địa điểm; chưa có kết nối Internet thực hay kiểm thử in tài liệu. Nếu chọn phần mở rộng, nên làm trên một bản sao và ghi riêng phép thử được phép/bị chặn.

Mã dựng ban đầu và dữ liệu tạm nằm trong `work/`, không cần nộp. File `.pkt` cuối đã được cấu hình và lưu lại bằng Packet Tracer; nên dùng trực tiếp file này cho việc học và chỉnh sửa.

Thư viện mã hóa/ghi định dạng được dùng để dựng thiết bị nền: [packet-tracer-pkt-format](https://github.com/aacanadaa/packet-tracer-pkt-format). Nội dung thiết kế, kế hoạch địa chỉ và trang web do bản dự án này xây dựng riêng.
