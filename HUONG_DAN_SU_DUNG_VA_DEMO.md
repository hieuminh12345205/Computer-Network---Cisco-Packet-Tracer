# Hướng dẫn sử dụng và kịch bản demo

Dự án: **Thiết kế mạng Trung tâm Đào tạo Minh An** — CSE3030 Mạng máy tính và truyền thông
Phần mềm: **Cisco Packet Tracer 9.0.1.0858**

---

## 0. Thông tin cần nhớ trước khi mở máy

| Mục | Giá trị |
|---|---|
| File phương án cơ bản | `CSE3030_2_Nhom6_MinhAn.pkt` |
| File phần mở rộng | `CSE3030_2_Nhom6_MinhAn_MoRong_ACL.pkt` |
| Website nội bộ | `http://portal.minhan.test` |
| Wi-Fi giảng viên | SSID `MINHAN-TEACHER` — WPA2-PSK/AES — khóa `MinhAnLab2026!` |
| Máy in dùng chung | `172.22.10.6` |
| Máy chủ DNS + HTTP | `172.22.10.5` |
| Gateway LAN A / LAN B | `172.22.10.1` / `172.22.20.1` |

**Tài khoản quản trị thiết bị** (router và hai switch dùng chung):

| Mục | Giá trị |
|---|---|
| Username | `admin` |
| Password | `MinhAn@Admin26` |
| Enable secret | `MinhAn@Enable26` |

> Console và VTY đều đặt `login local`. Khi mở tab **CLI** của router/switch sẽ phải đăng
> nhập trước. Nếu quên mật khẩu trong lúc trình bày thì không vào được thiết bị, nên hãy
> để sẵn bảng này cạnh máy. Đây là mật khẩu thử nghiệm của bài tập, không dùng cho hệ
> thống thật.

---

## 1. Mở file và chờ mạng hội tụ

1. Mở Packet Tracer **9.0.1** → `File > Open` → chọn `CSE3030_2_Nhom6_MinhAn.pkt`.
2. Giữ chế độ **Logical** và **Realtime** (góc dưới bên phải).
3. Chờ **10–20 giây**, hoặc bấm **Fast Forward Time** (phím `Alt+D`) vài lần, cho tới khi:
   - tất cả đầu cáp chuyển sang **chấm xanh lá** (Spanning Tree đã hội tụ),
   - hai laptop hiện sóng Wi-Fi nối tới `AP-GIANGVIEN`,
   - các PC đã xin xong DHCP.
4. Nếu cửa sổ nhỏ không thấy đủ hai khu: phóng to cửa sổ hoặc dùng **Zoom Out**.

> Đừng kết luận mạng lỗi khi vừa mở file. Lúc này ARP và DHCP chưa xong, Simple PDU
> đầu tiên rất hay báo **Failed**. Gửi lại lần hai là đúng cách làm, không phải là che lỗi.

---

## 2. Kịch bản demo — 8 bước, khoảng 10 phút

Thứ tự dưới đây đi từ tầng thấp lên tầng cao, mỗi bước chứng minh đúng một ý.
Cột **Nói gì** là câu chốt nên nói khi trình bày.

### Bước 1 — Giới thiệu sơ đồ (1 phút)

| Thao tác | Nói gì |
|---|---|
| Để nguyên màn hình Logical, chỉ vào từng cụm | "Trung tâm có khoảng 30 người dùng, chia hai khu. LAN A là khu Giáo vụ `172.22.10.0/27`, LAN B là khu Phòng học `172.22.20.0/26`. Hai khu nối vào hai cổng khác nhau của router `R-MA` nên là hai miền quảng bá riêng." |

Chỉ rõ các nhãn ghi chú trên sơ đồ — chúng ghi đúng subnet, mask, gateway và dải DHCP
như trong cấu hình thực tế.

### Bước 2 — DHCP cấp đúng thông số (1 phút)

| Thao tác | Kết quả mong đợi |
|---|---|
| `PC-HV1` → **Desktop > IP Configuration** → chọn **DHCP** | IP thuộc `172.22.20.10–.59`, Mask `255.255.255.192`, Gateway `172.22.20.1`, DNS `172.22.10.5` |
| Mở thêm `PC-GV1` để so sánh | IP thuộc `172.22.10.10–.29`, Gateway `172.22.10.1`, **DNS vẫn là `172.22.10.5`** |

> **Nói gì:** "DHCP chạy ngay trên router với hai pool riêng. DNS của cả hai khu đều trỏ về
> một máy chủ duy nhất ở LAN A, nên máy ở LAN B bắt buộc phải đi qua gateway mới hỏi được
> tên miền — đó là lý do phải có định tuyến giữa hai subnet."

Bổ sung trên router nếu giảng viên muốn xem phía máy chủ:

```
show ip dhcp binding
show ip dhcp pool
```

### Bước 3 — Liên lạc trong cùng một LAN (1 phút)

Mở **Command Prompt** của `PC-GV1`:

```
ipconfig
ping 172.22.10.1
```

| Phép thử | Mong đợi |
|---|---|
| `ping` gateway LAN A | 4/4 phản hồi |
| `ping` sang `PC-GV2` (đọc IP thật của máy đó trước) | 4/4 phản hồi, gói đầu có thể mất do ARP |

> **Nói gì:** "Trong cùng LAN, switch chuyển khung theo địa chỉ MAC, gói không cần qua router."

### Bước 4 — Liên lạc giữa hai LAN (1 phút)

Trên `PC-HV1`:

```
ping 172.22.10.5
tracert 172.22.10.5
```

| Phép thử | Mong đợi |
|---|---|
| `ping` tới máy chủ ở LAN A | 4/4 phản hồi |
| `tracert` | Hiện **2 chặng**: `172.22.20.1` rồi `172.22.10.5` |

> **Nói gì:** "`tracert` cho thấy rõ gói đi qua đúng một router. Hai mạng nằm trong bảng
> định tuyến dưới dạng *connected*, không cần giao thức định tuyến động vì cả hai đều nối
> trực tiếp vào `R-MA`."

Minh chứng phía router:

```
show ip route
show ip interface brief
```

Chỉ vào hai dòng `C` trong bảng định tuyến và trạng thái `up/up` của `G0/0`, `G0/1`.

### Bước 5 — DNS và website nội bộ (2 phút)

| Thao tác | Mong đợi |
|---|---|
| `PC-GV1` → **Desktop > Web Browser** → `http://portal.minhan.test` | Hiện trang cổng thông tin Minh An |
| `PC-HV1` → cùng địa chỉ | Hiện đúng trang đó, chứng minh client LAN B qua được router |

> **Nói gì:** "Server chạy đồng thời hai dịch vụ. DNS giữ bản ghi A `portal.minhan.test`
> trỏ về `172.22.10.5`, HTTP phục vụ trang nội bộ. Thứ tự xảy ra là **DNS → bắt tay TCP → HTTP**."

Muốn chứng minh DNS thật sự có tác dụng: trên `PC-HV1` mở `http://172.22.10.5` — ra cùng
một trang. Vào được bằng cả IP lẫn tên miền nghĩa là phần phân giải tên đang hoạt động,
không phải trang được nhúng sẵn trong trình duyệt.

### Bước 6 — Wi-Fi và máy in dùng chung (1,5 phút)

| Thao tác | Mong đợi |
|---|---|
| `LT-GV2` → **Desktop > PC Wireless > Connect** | Đã nối `MINHAN-TEACHER`, bảo mật WPA2-PSK |
| `LT-GV2` → **IP Configuration** | Nhận DHCP trong dải LAN B |
| `LT-GV2` → **Command Prompt** → `ping 172.22.10.6` | 4/4 phản hồi từ máy in |
| `LT-GV2` → **Web Browser** → `http://portal.minhan.test` | Mở được trang nội bộ |

> **Nói gì:** "Access Point đóng vai trò cầu nối lớp 2 vào LAN B, nên laptop nằm cùng subnet
> với các PC phòng học và cũng nhận IP từ pool `PHONGHOC`. Gói từ laptop tới máy in đi qua
> AP, qua switch, lên router rồi mới sang khu Giáo vụ."

### Bước 7 — Quan sát gói tin trong Simulation Mode (2 phút)

1. Chuyển sang **Simulation**.
2. **Edit Filters** → chỉ giữ **ICMP** và **ARP**.
3. Tạo **Simple PDU** từ `PC-GV1` tới `PC-HV3`.
4. Bấm **Capture / Forward** từng bước và đọc đường đi:

```
PC-GV1 → SW-GIAOVU → R-MA → SW-PHONGHOC → PC-HV3
```

phản hồi đi ngược lại đúng tuyến đó.

> **Nói gì:** "Nếu chưa biết MAC của gateway thì ARP chạy trước ICMP. Switch chỉ chuyển tiếp
> khung Ethernet, còn router mới là nơi gói được chuyển giữa hai subnet — nhìn vào PDU sẽ thấy
> MAC đích đổi ở mỗi chặng trong khi IP đích thì giữ nguyên."

Muốn demo luồng web: thêm **DNS** và **HTTP** vào Edit Filters rồi mở trang từ `PC-HV1`,
sẽ thấy lần lượt DNS query → DNS response → TCP SYN/SYN-ACK/ACK → HTTP.

### Bước 8 — Chứng minh cấu hình bền vững (0,5 phút)

Đóng file, mở lại, chờ hội tụ rồi mở lại trang web một lần nữa.

> **Nói gì:** "Cấu hình đã được `copy running-config startup-config` nên nạp lại file vẫn
> chạy. Địa chỉ DHCP cụ thể có thể đổi theo thứ tự xin cấp phát, nhưng subnet, gateway và
> dịch vụ thì không đổi."

---

## 3. Demo phần mở rộng — ACL (3 phút)

Mở **`CSE3030_2_Nhom6_MinhAn_MoRong_ACL.pkt`**. Đây là bản sao của phương án cơ bản, thêm ACL và
port-security. Giữ hai file tách nhau vì phương án cơ bản yêu cầu hai LAN liên lạc được,
còn phần mở rộng thì cố tình chặn bớt.

Chi tiết cấu hình, bảng kiểm thử và cách giải thích nằm trong [`MO_RONG_ACL.md`](MO_RONG_ACL.md).
Tóm tắt phần cần bấm:

| Thao tác trên `PC-HV1` | Mong đợi | Ý nghĩa |
|---|---|---|
| `http://portal.minhan.test` | **Mở được** | ACL cho phép DNS + HTTP tới máy chủ |
| `ping 172.22.10.6` | **4/4 phản hồi** | Máy in vẫn dùng chung được |
| `ping 172.22.10.5` | **Bị chặn** | Mở web không có nghĩa là mở mọi thứ: ACL lọc theo *dịch vụ*, không chỉ theo địa chỉ |
| `ping` tới `PC-GV1` | **Bị chặn** | Học viên không chọc được vào máy trạm khu Giáo vụ |

Sau đó vào CLI của `R-MA`:

```
show access-lists
```

Chỉ vào cột số lần khớp (`match`) tăng dần sau mỗi phép thử — đây là bằng chứng ACL thực
sự đang xử lý gói, chứ không chỉ nằm trong cấu hình.

---

## 4. Xử lý sự cố khi demo

| Hiện tượng | Nguyên nhân thường gặp | Cách xử lý |
|---|---|---|
| Simple PDU đầu tiên **Failed** | ARP/DHCP chưa xong | Bấm Fast Forward Time rồi gửi lại. Đây là hành vi bình thường. |
| PC không có IP | Chưa chọn DHCP, hoặc cáp chưa lên | Desktop > IP Configuration > chọn **DHCP**; kiểm tra đầu cáp đã xanh |
| Mở trang web báo không tìm thấy | Gõ nhầm, hoặc DNS chưa có trong máy trạm | Kiểm tra DNS trong IP Configuration phải là `172.22.10.5`; thử `http://172.22.10.5` để tách lỗi DNS khỏi lỗi HTTP |
| Laptop không thấy Wi-Fi | Sai khóa, hoặc ngoài vùng phủ | Nhập lại `MinhAnLab2026!` (có dấu `!` ở cuối); kéo laptop lại gần AP |
| Vào CLI bị hỏi mật khẩu | Đúng như thiết kế, `login local` | Dùng `admin` / `MinhAn@Admin26` (privilege 15, vào thẳng `#`). `MinhAn@Enable26` chỉ cần khi `enable` từ dấu `>` |
| `ping` tới `172.22.10.5` thất bại | Đang mở **nhầm file mở rộng** | ACL cố ý chặn ICMP tới máy chủ. Mở `CSE3030_2_Nhom6_MinhAn.pkt` nếu muốn demo phương án cơ bản. |
| Mở file báo lỗi phiên bản | File lưu bằng 9.0.1 | Mở bằng Packet Tracer 9.0.1 trở lên |

---

## 5. Câu hỏi giảng viên hay hỏi, và câu trả lời

**Vì sao chia `/27` và `/26` mà không dùng `/24` cho gọn?**
Vì quy mô hai khu khác nhau: Giáo vụ khoảng 8 người nên `/27` (30 địa chỉ host) là đủ và còn
dư cho hạ tầng tĩnh; Phòng học khoảng 22 người nên `/26` (62 địa chỉ host). Chia theo nhu cầu
thật thì tiết kiệm địa chỉ và thể hiện được việc tính toán subnet, thay vì cấp dư gấp mười lần.

**Vì sao không cần giao thức định tuyến?**
Cả hai mạng đều nối trực tiếp vào `R-MA` nên xuất hiện trong bảng định tuyến dưới dạng
*connected* ngay khi bật cổng. Giao thức định tuyến chỉ cần khi có mạng ở xa phải học qua
router khác.

**DHCP đặt trên router hay trên server thì hơn?**
Ở mô hình này đặt trên router gọn hơn vì router đã là gateway của cả hai subnet, không cần
`ip helper-address` để chuyển tiếp bản tin DHCP qua lại. Nếu hệ thống lớn hơn, nhiều site,
thì tách DHCP ra máy chủ riêng sẽ dễ quản lý tập trung hơn.

**Vì sao máy in và máy chủ dùng IP tĩnh?**
Vì chúng là tài nguyên được tra cứu theo địa chỉ cố định. Hai IP này nằm trong dải đã
`ip dhcp excluded-address` nên DHCP không bao giờ cấp trùng.

**Dải DHCP `.10–.29` lấy ở đâu ra?**
`/27` cho host `.1–.30`. Loại trừ `.1–.9` (dành cho gateway, switch, server, máy in và dự phòng)
và `.30`, phần còn lại là `.10–.29`. Tương tự LAN B loại trừ `.1–.9` và `.60–.62` còn `.10–.59`.

**Chia subnet có chặn được truy cập giữa hai khu không?**
Không. Chia subnet chỉ tách miền quảng bá. Muốn chặn thì phải dùng ACL — đó chính là nội dung
của phần mở rộng.

**Vì sao chỉ đặt 6 PC khi có 30 người dùng?**
6 PC, 2 laptop là **thiết bị đại diện** theo mức tối thiểu của đề bài, đủ để kiểm thử liên lạc
trong cùng LAN và giữa hai LAN. Kế hoạch địa chỉ mới là chỗ thể hiện quy mô 30 người: dải DHCP
đã tính đủ chỗ cho toàn bộ người dùng thật.
