# Dàn ý báo cáo — CSE3030, lớp 2, nhóm 6: Mạng Trung tâm Đào tạo Minh An

> File này là **khung để nhóm tự viết**, không phải báo cáo nộp. Mỗi mục ghi: *viết gì*, *lấy số liệu/ảnh ở đâu trong repo*, và *độ dài gợi ý*.
> Tổng độ dài gợi ý: **12–18 trang A4** (chưa tính phụ lục), Times New Roman 13, giãn dòng 1.3.
>
> ⚠️ Repo không chứa đề bài gốc. Trước khi viết, **đối chiếu dàn ý này với đề / rubric của giảng viên**. Nếu đề bắt buộc mục nào mà dàn ý chưa có, thêm vào; nếu đề quy định thứ tự chương, theo đề.

---

## Trang bìa (1 trang)

- Trường, khoa, môn **CSE3030 – Mạng máy tính**, lớp 2.
- Tên đề tài: *Thiết kế và mô phỏng hệ thống mạng cho Trung tâm Đào tạo Minh An bằng Cisco Packet Tracer*.
- Nhóm 6: họ tên và MSSV từng thành viên. Giảng viên hướng dẫn. Tháng/năm.

## Bảng phân công công việc (½ trang)

| STT | Họ tên | MSSV | Nhiệm vụ | Mức độ hoàn thành |
|---|---|---|---|---|
| 1 | | | Phân tích yêu cầu, quy hoạch IP | 100% |
| 2 | | | Dựng topology, cấu hình router/DHCP | |
| 3 | | | Server DNS/Web, máy in, Wi-Fi | |
| 4 | | | Phần mở rộng ACL + port-security | |
| 5 | | | Kiểm thử, chụp minh chứng, viết báo cáo | |

*(Sửa vai trò cho khớp số người và việc mỗi người thực sự làm.)*

## Mục lục, danh mục hình, danh mục bảng

Tạo tự động trong Word: *References → Table of Contents* và *Insert Table of Figures*. Muốn tạo tự động thì mọi tiêu đề phải dùng style Heading, mọi chú thích hình/bảng phải dùng *Insert Caption*.

---

## Chương 1. Giới thiệu và phân tích yêu cầu (1,5–2 trang)

### 1.1 Giới thiệu đơn vị
- Trung tâm Minh An có khoảng 30 người dùng, chia làm 2 khu: **Giáo vụ** (~8 người) và **Phòng học** (~22 người: học viên và giảng viên).
- Nguồn: [`README.md`](README.md) §1, [`THIET_KE_VA_HUONG_DAN.md`](THIET_KE_VA_HUONG_DAN.md) §1.

### 1.2 Nhu cầu sử dụng
Liệt kê thành gạch đầu dòng, mỗi nhu cầu nối với một giải pháp ở Chương 2:
- Hai khu tách mạng riêng nhưng vẫn liên lạc được với nhau.
- Máy trạm tự nhận IP, không phải cấu hình tay.
- Có cổng thông tin nội bộ truy cập bằng tên miền `portal.minhan.test`.
- Có máy in dùng chung cho cả hai khu.
- Giảng viên dùng laptop qua Wi-Fi có mật khẩu.
- Thiết bị mạng phải có mật khẩu quản trị.

### 1.3 Phạm vi và giả định
- Mỗi khu chỉ đặt 3 PC (cộng 2 laptop) làm **thiết bị đại diện**. Kế hoạch IP vẫn tính đủ quy mô thật.
- Không kết nối Internet.
- Mô phỏng trên Packet Tracer 9.0.1.
- Phần mở rộng ACL được làm ở một file `.pkt` riêng. Giải thích lý do: phương án cơ bản cần hai LAN liên lạc tự do, còn phần mở rộng cố ý chặn bớt.

---

## Chương 2. Thiết kế mạng (3–4 trang)

### 2.1 Sơ đồ tổng thể
- **Hình 2.1:** [`minh_chung/01_SoDo_TongThe.png`](minh_chung/01_SoDo_TongThe.png).
- Viết 1 đoạn giải thích: router R-MA ở giữa, mỗi cổng nối một switch, mỗi switch phục vụ một khu, AP gắn vào switch Phòng học.
- Lý do chọn mô hình 1 router, 2 LAN: quy mô nhỏ; chia 2 subnet thì broadcast của khu này không lan sang khu kia; mỗi khu dễ áp chính sách riêng (như ACL ở Chương 5).

### 2.2 Danh mục thiết bị
- **Bảng 2.1:** copy từ [`README.md`](README.md) §3, 14 thiết bị.
- Thêm một cột "Lý do chọn". Ví dụ: 2911 có 3 cổng Gigabit và chạy được DHCP; 2960 là switch Lớp 2 truy cập, đủ 24 cổng.

### 2.3 Bảng nối cổng
- **Bảng 2.2:** copy từ [`README.md`](README.md) §3, "Bảng kết nối cổng cáp".
- Giải thích vì sao dùng cáp thẳng: router–switch và switch–PC là hai thiết bị khác loại.

### 2.4 Kế hoạch địa chỉ IPv4 — **phần giảng viên hay chấm kỹ nhất**
- Dùng dải riêng 172.16.0.0/12 theo RFC 1918 [1].
- **Trình bày cách tính, không chỉ đưa kết quả:**
  - LAN A cần khoảng 8 host cộng dự phòng → chọn /27 = 32 địa chỉ, 30 dùng được (2⁵ − 2).
  - LAN B cần khoảng 22 host cộng dự phòng → /28 chỉ có 14 là không đủ → chọn /26 = 62 dùng được.
- **Bảng 2.3:** network, mask, dải dùng được, broadcast, gateway (copy [`README.md`](README.md) §4).
- **Bảng 2.4:** IP tĩnh: gateway `.1`, switch quản trị `.2`, SRV-PORTAL `.5`, máy in `.6`; dải DHCP `.10–.29` / `.10–.59`.
- Giải thích quy ước: các địa chỉ đầu dải để cho thiết bị hạ tầng, nên DHCP không cấp trùng.

---

## Chương 3. Cấu hình thiết bị và dịch vụ (3–4 trang)

Mỗi mục gồm: **mục đích (1–2 câu) → đoạn lệnh chính (khung code, font Consolas) → giải thích vài dòng quan trọng**. **Không dán nguyên file config.** File đầy đủ để ở phụ lục.

| Mục | Nội dung | Lấy lệnh từ |
|---|---|---|
| 3.1 Cấu hình cơ bản và bảo mật quản trị | hostname, `enable secret`, `username admin`, `login local` trên console/VTY, banner, `service password-encryption` | [`R-MA.txt`](R-MA.txt), [`SW-GIAOVU.txt`](SW-GIAOVU.txt) |
| 3.2 Interface router | IP của G0/0 và G0/1, `no shutdown` | [`R-MA.txt`](R-MA.txt) |
| 3.3 DHCP trên router | `ip dhcp excluded-address`, 2 pool (network, default-router, dns-server). Giải thích quá trình DORA [2] | [`R-MA.txt`](R-MA.txt) |
| 3.4 Switch | IP quản trị trên VLAN 1, `ip default-gateway` | [`SW-*.txt`](SW-GIAOVU.txt) |
| 3.5 Server DNS + Web | Bản ghi A `portal.minhan.test → 172.22.10.5`, bật HTTP. Nêu vai trò của DNS [3] | Ảnh tab Services (chụp thêm nếu cần) |
| 3.6 Máy in | IP tĩnh, kèm lý do dùng IP tĩnh | |
| 3.7 Wi-Fi | SSID `MINHAN-TEACHER`, WPA2-PSK/AES, laptop gắn card WPC300N. Nêu chuẩn 802.11 và WPA2 [4] | ảnh 11, 12 |

> Mật khẩu: báo cáo có thể ghi mật khẩu thử nghiệm như README đã ghi. Nếu giảng viên không muốn, thay bằng `********` và để ở phụ lục.

---

## Chương 4. Kiểm thử và đánh giá (3–4 trang)

### 4.1 Phương pháp
- Dùng các công cụ: `ipconfig`, `ping`, `tracert`, `nslookup`, Web Browser, chế độ Simulation, và các lệnh `show` trên router.
- Nêu quy ước đọc TTL: 128 nghĩa là cùng LAN, 127 nghĩa là qua 1 router, 255 nghĩa là router trả lời. Cơ sở là ICMP [5].

### 4.2 Bảng kiểm thử
- **Bảng 4.1:** copy từ [`BANG_KIEM_THU.md`](BANG_KIEM_THU.md), giữ các cột *STT, nguồn, đích, thao tác, kết quả mong đợi, kết quả thực tế, minh chứng*. Ở cột minh chứng ghi "Hình 4.x", không ghi tên file.

### 4.3 Minh chứng
Mỗi nhóm chọn 1–2 ảnh tiêu biểu đưa vào thân báo cáo. Ảnh còn lại để ở Phụ lục B.

| Nhóm | Ảnh gợi ý |
|---|---|
| DHCP | 02, 04, 06, 28 |
| Liên lạc trong LAN / qua router | 25, 26, 27 |
| DNS + Web | 08, 09, 10, 13 |
| Wi-Fi | 11, 12 |
| Máy in | 14, 15, 16 |
| Simulation | 17 |
| Quản trị (login, telnet) | 18, 29 |

Mỗi ảnh kèm chú thích và **1–2 câu đọc kết quả**. Ví dụ: "PC-HV1 nhận 172.22.20.x/26, gateway .1, DNS 172.22.10.5 → DHCP pool PHONGHOC hoạt động."

### 4.4 Đánh giá
Đối chiếu từng nhu cầu ở §1.2 với kết quả kiểm thử. Có thể dùng bảng 3 cột: *nhu cầu → giải pháp → test số mấy chứng minh*.

---

## Chương 5. Phần mở rộng: ACL và port-security (2–3 trang)

Nguồn chính: [`MO_RONG_ACL.md`](MO_RONG_ACL.md). Tài liệu tham khảo: [6], [7].

### 5.1 Bài toán
Học viên không được truy cập trực tiếp vào máy của Giáo vụ. Học viên chỉ được dùng portal và máy in.

### 5.2 Thiết kế ACL
- Dùng extended ACL, đặt **inbound trên G0/1**, tức gần nguồn. Giải thích vì sao đặt gần nguồn.
- **Bảng 5.1:** 7 dòng ACL (10 → 70) kèm ý nghĩa từng dòng.

### 5.3 Vấn đề ACL stateless — **điểm cộng nếu viết tốt**
Kể lại đúng như đã xảy ra: lần test đầu, E6 thất bại.
- Hiện tượng: PC-GV1 ping PC-HV1 bị timeout.
- Nguyên nhân: echo-reply từ LAN B đi về bị dòng `deny` chặn, vì ACL không nhớ trạng thái kết nối.
- Cách xử lý: thêm `permit icmp … echo-reply` và `permit tcp … established`.
- Kết quả test lại: 4/4 reply, trong khi học viên vẫn bị chặn như yêu cầu.

Đoạn này cho thấy nhóm hiểu bản chất, không chỉ chép cấu hình.

### 5.4 Port-security
Đặt trên SW-PHONGHOC F0/1–3: sticky MAC, `maximum 1`, chế độ violation. Kèm ảnh 24.

### 5.5 Kiểm thử E1–E8
- **Bảng 5.2:** copy từ [`MO_RONG_ACL.md`](MO_RONG_ACL.md).
- Ảnh 19–23, 30, 31. Ảnh 23 là `show access-lists` có số lượt match.

---

## Chương 6. Kết luận (1 trang)

- **Đạt được:** liệt kê ngắn, khớp với §1.2.
- **Hạn chế còn lại** (trung thực). Gợi ý:
  - Chưa có VLAN hay dự phòng: router và switch đều là điểm lỗi đơn (single point of failure).
  - Telnet truyền mật khẩu dạng rõ, nên chuyển sang SSH.
  - DNS/Web chỉ nằm trên 1 server.
  - Không mô phỏng kết nối Internet/NAT.
  - Port-security ghi MAC cố định, nên thay máy thì phải xóa sticky MAC.
  - Chưa chụp Simulation cho DNS/HTTP (#30) và so sánh running với startup config (#32). Bỏ dòng này nếu sau đó đã chụp bổ sung.
- **Hướng phát triển:** VLAN và inter-VLAN routing, SSH, NAT ra Internet, server dự phòng, WPA2-Enterprise/RADIUS.

---

## Tài liệu tham khảo

Trích dẫn kiểu IEEE: số trong ngoặc vuông ở thân bài, danh sách cuối báo cáo. **Chỉ giữ những mục thực sự được trích trong bài.**

**Tiêu chuẩn (RFC, IEEE)**

[1] Y. Rekhter *et al.*, "Address Allocation for Private Internets," RFC 1918, IETF, 1996. https://www.rfc-editor.org/rfc/rfc1918

[2] R. Droms, "Dynamic Host Configuration Protocol," RFC 2131, IETF, 1997. https://www.rfc-editor.org/rfc/rfc2131

[3] P. Mockapetris, "Domain Names – Implementation and Specification," RFC 1035, IETF, 1987. https://www.rfc-editor.org/rfc/rfc1035

[4] IEEE, *IEEE Standard for Information Technology – Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications*, IEEE Std 802.11. Dùng cho Wi-Fi; phần bảo mật WPA2/CCMP-AES có nguồn gốc từ bản sửa đổi 802.11i.

[5] J. Postel, "Internet Control Message Protocol," RFC 792, IETF, 1981. https://www.rfc-editor.org/rfc/rfc792

[8] V. Fuller and T. Li, "Classless Inter-domain Routing (CIDR)," RFC 4632, IETF, 2006. https://www.rfc-editor.org/rfc/rfc4632 — dùng khi giải thích ký hiệu /27, /26.

[9] R. Fielding *et al.*, "HTTP Semantics," RFC 9110, IETF, 2022. https://www.rfc-editor.org/rfc/rfc9110 — dùng nếu có viết về HTTP.

**Tài liệu Cisco**

[6] Cisco Networking Academy, *CCNA: Enterprise Networking, Security, and Automation* (v7). Đọc các phần về ACL: khái niệm, standard/extended ACL, nơi đặt ACL.

[7] Cisco Networking Academy, *CCNA: Switching, Routing, and Wireless Essentials* (v7). Đọc các phần DHCPv4, Switch Security (port-security) và WLAN.

[10] Cisco Networking Academy, *CCNA: Introduction to Networks* (v7). Đọc phần IPv4 addressing / subnetting và cấu hình thiết bị cơ bản.

[11] Cisco Systems, *Cisco Packet Tracer*, phiên bản 9.0.1. https://www.netacad.com/cisco-packet-tracer

[12] Cisco Systems, tài liệu cấu hình IOS trên cisco.com. Tìm theo tên: "Configuring DHCP" (IOS IP Addressing Configuration Guide), "IP Access List" (Security Configuration Guide), "Configuring Port Security" (Catalyst 2960 Software Configuration Guide).

**Giáo trình**

[13] J. F. Kurose and K. W. Ross, *Computer Networking: A Top-Down Approach*, 8th ed. Pearson, 2021. Chương 4 (Network Layer: IPv4, DHCP, subnet) và Chương 7 (Wireless).

[14] A. S. Tanenbaum, N. Feamster and D. Wetherall, *Computer Networks*, 6th ed. Pearson, 2021.

> Nếu môn học có giáo trình hoặc slide riêng của giảng viên, đặt lên đầu danh sách. Giảng viên thường thích thấy tài liệu của chính môn học được trích.
> Khi sắp xếp lại số thứ tự, đánh lại số liên tục [1], [2], … theo thứ tự xuất hiện trong bài.

---

## Phụ lục

- **A.** Cấu hình đầy đủ: [`R-MA.txt`](R-MA.txt), [`SW-GIAOVU.txt`](SW-GIAOVU.txt), [`SW-PHONGHOC.txt`](SW-PHONGHOC.txt); bản mở rộng [`R-MA_MoRong_ACL.txt`](R-MA_MoRong_ACL.txt), [`SW-PHONGHOC_MoRong_PortSecurity.txt`](SW-PHONGHOC_MoRong_PortSecurity.txt).
- **B.** Các ảnh minh chứng còn lại trong `minh_chung/`.
- **C.** Hướng dẫn mở file và tài khoản đăng nhập, rút gọn từ [`HUONG_DAN_NHANH.md`](HUONG_DAN_NHANH.md).

---

## Checklist trước khi nộp

- [ ] Mọi hình và bảng đều có số và chú thích, và **được nhắc tới trong văn bản** ("như Hình 2.1").
- [ ] Ảnh dễ đọc: crop sát vùng cần xem, chữ trong CLI đọc được khi in.
- [ ] Số liệu trong báo cáo khớp với file `.pkt` nộp kèm: IP, tên thiết bị, 7 dòng ACL.
- [ ] Không dán nguyên file config vào thân bài.
- [ ] Tên file báo cáo theo quy ước lớp, ví dụ `CSE3030_2_Nhom6_BaoCao.docx`. Hỏi lại quy ước nếu chưa chắc.
- [ ] Xuất thêm bản PDF để tránh lệch font.
