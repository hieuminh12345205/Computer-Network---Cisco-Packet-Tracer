# Phần mở rộng: ACL giới hạn truy cập giữa hai bộ phận

File: **`CSE3030_2_Nhom6_MinhAn_MoRong_ACL.pkt`**
Cấu hình xuất ra: [`R-MA_MoRong_ACL.txt`](R-MA_MoRong_ACL.txt),
[`SW-PHONGHOC_MoRong_PortSecurity.txt`](SW-PHONGHOC_MoRong_PortSecurity.txt)

Đề bài cho chọn **một** nội dung mở rộng: chia VLAN và định tuyến liên VLAN; ACL giới hạn
truy cập giữa các bộ phận; NAT/PAT qua router ISP mô phỏng; hoặc kết nối hai chi nhánh.
Dự án này chọn **ACL**.

---

## 1. Vì sao chọn ACL

Phương án cơ bản đã có hai subnet nối qua hai cổng router, mỗi khu một switch. Đây là cách
bố trí hợp lý và **không cần đổi sang VLAN + trunk** — chuyển sang router-on-a-stick sẽ phải
dựng lại gần như toàn bộ sơ đồ mà không giải quyết thêm vấn đề nào.

Vấn đề còn tồn tại sau phương án cơ bản là: chia subnet chỉ tách **miền quảng bá**, nó không
hề chặn truy cập. Học viên ngồi ở Phòng học vẫn ping và truy cập được thẳng vào mọi máy
trạm của khu Giáo vụ — nơi chứa hồ sơ học viên. ACL xử lý đúng vấn đề đó với chi phí thấp
nhất, nên đây là phần mở rộng tự nhiên nhất của chính thiết kế này.

## 2. Mục tiêu cụ thể

Từ khu Phòng học (`172.22.20.0/26`) hướng về khu Giáo vụ (`172.22.10.0/27`):

| Phải cho phép | Phải chặn |
|---|---|
| Phân giải tên miền tới máy chủ (DNS/UDP 53) | Mọi truy cập khác vào khu Giáo vụ |
| Truy cập cổng thông tin nội bộ (HTTP/TCP 80) | Ping và truy cập tới các PC Giáo vụ |
| Dùng chung máy in `172.22.10.6` (mọi giao thức) | Ping tới chính máy chủ |

Chiều ngược lại — Giáo vụ sang Phòng học — **không bị giới hạn**, vì nhân sự giáo vụ cần hỗ
trợ kỹ thuật cho phòng học.

## 3. Cấu hình

```
ip access-list extended PHONGHOC-IN
 remark Khu Phong hoc chi duoc dung DNS/Web va may in cua khu Giao vu
 permit udp 172.22.20.0 0.0.0.63 host 172.22.10.5 eq domain
 permit tcp 172.22.20.0 0.0.0.63 host 172.22.10.5 eq www
 permit ip 172.22.20.0 0.0.0.63 host 172.22.10.6
 permit icmp 172.22.20.0 0.0.0.63 172.22.10.0 0.0.0.31 echo-reply
 permit tcp 172.22.20.0 0.0.0.63 172.22.10.0 0.0.0.31 established
 deny ip 172.22.20.0 0.0.0.63 172.22.10.0 0.0.0.31
 permit ip any any
```

```
interface GigabitEthernet0/1
 ip access-group PHONGHOC-IN in
```

Kèm theo, bật port-security trên ba cổng nối PC của `SW-PHONGHOC`:

```
interface range FastEthernet0/1 - 3
 switchport port-security
 switchport port-security maximum 1
 switchport port-security violation restrict
 switchport port-security mac-address sticky
```

## 4. Giải thích từng điểm — phần hay bị hỏi

**Vì sao đặt ở `G0/1` chiều `in`?**
`G0/1` là cổng router hướng về khu Phòng học. Lọc ngay ở chiều `in` nghĩa là gói bị loại
ngay khi vừa vào router, trước khi tốn công tra bảng định tuyến. Nếu đặt ở chiều `out` của
`G0/0` thì cũng chặn được, nhưng sẽ chặn nhầm cả lưu lượng từ nguồn khác đi vào LAN A.

**Vì sao không cần ACL cho chiều phản hồi?**
Vì ACL chỉ áp một chiều `in` trên `G0/1`. Gói phản hồi từ máy chủ đi **ra** cổng `G0/1` nên
không bị kiểm tra. Nhờ vậy DNS response và dữ liệu HTTP vẫn về được máy trạm bình thường.

**Thế còn lúc Giáo vụ chủ động liên lạc sang Phòng học?**
Lúc này chiều đi và chiều về đổi chỗ. Gói từ Giáo vụ đi **ra** `G0/1` nên không bị kiểm tra,
nhưng gói **phản hồi** của máy học viên lại đi **vào** `G0/1` với nguồn `172.22.20.x`, đích
`172.22.10.x`. ACL mở rộng **không nhớ trạng thái kết nối**, nên nếu không có luật riêng thì
phản hồi này khớp dòng `deny` và bị huỷ (đây chính là lỗi phép thử E6 ở lần chạy đầu).
Hai dòng thêm vào trước `deny` xử lý việc đó:
- `permit icmp ... echo-reply`: chỉ cho **gói trả lời ping** đi qua. Học viên vẫn không tự
  ping sang Giáo vụ được, vì gói của họ là `echo` (yêu cầu), không phải `echo-reply`.
- `permit tcp ... established`: chỉ cho gói TCP có cờ ACK hoặc RST, tức là gói thuộc một phiên
  **đã có sẵn**. Gói mở phiên mới (chỉ có cờ SYN) từ học viên vẫn bị chặn.

**Wildcard mask tính thế nào?**
`/26` → wildcard `0.0.0.63`. `/27` → wildcard `0.0.0.31`. Wildcard là phần bù của subnet mask:
`255.255.255.192` → `0.0.0.63`; `255.255.255.224` → `0.0.0.31`.

**`eq domain` và `eq www` áp cho cổng nguồn hay cổng đích?**
Cổng đích, vì nó đứng **sau** địa chỉ đích trong câu lệnh. Cổng nguồn của máy trạm là cổng
ngẫu nhiên nên không thể và không nên chỉ định.

**Vì sao `ping` tới máy chủ bị chặn trong khi web vào được?**
Hai dòng `permit` đầu chỉ mở **UDP 53** và **TCP 80** tới máy chủ. ICMP không khớp dòng nào
trong số đó, cũng không phải máy in, nên rơi vào dòng `deny`. Đây là điểm demo đắt giá nhất:
nó cho thấy ACL mở rộng lọc theo **dịch vụ ở tầng 4**, không chỉ theo địa chỉ ở tầng 3.

**Dòng `permit ip any any` cuối để làm gì?**
Cuối mọi ACL luôn có `deny ip any any` ngầm định. Nếu không có dòng này, lưu lượng từ Phòng
học đi tới **mọi đích khác** (kể cả ra Internet sau này) đều bị chặn sạch. Dòng này giữ cho
ACL chỉ giới hạn đúng phạm vi khu Giáo vụ.

**Thứ tự các dòng có quan trọng không?**
Rất quan trọng. ACL được duyệt **tuần tự từ trên xuống, dừng ở dòng khớp đầu tiên**. Nếu đưa
`permit ip any any` lên trước dòng `deny` thì dòng `deny` vĩnh viễn không bao giờ được dùng
tới và ACL mất tác dụng hoàn toàn, dù `show access-lists` vẫn hiển thị đầy đủ. Đây là lỗi
phổ biến nhất khi viết ACL.

**Port-security làm gì và vì sao không áp cho cổng nối AP?**
Mỗi cổng PC chỉ học một địa chỉ MAC; cắm thêm switch lạ hay đổi máy khác vào sẽ bị từ chối.
Chọn `violation restrict` thay vì `shutdown` để cổng không tự tắt hẳn khi vi phạm — an toàn
hơn khi demo. **Không** áp cho `F0/4` vì đó là cổng nối `AP-GIANGVIEN`: mọi laptop Wi-Fi đều
gửi khung qua cổng này, giới hạn một MAC sẽ chặn mất toàn bộ mạng không dây.

## 5. Bảng kiểm thử phần mở rộng

Chạy trên `CSE3030_2_Nhom6_MinhAn_MoRong_ACL.pkt`, sau khi mạng đã hội tụ.

| # | Nguồn | Đích / thao tác | Kết quả mong đợi | Kết quả thực tế | Minh chứng |
|---|---|---|---|---|---|
| E1 | PC-HV1 | `http://portal.minhan.test` | Mở được trang — trường hợp **được phép** | Đạt: trang portal hiện đầy đủ | [`19_ACL_Web_DuocPhep`](minh_chung/19_ACL_Web_DuocPhep.png) |
| E2 | PC-HV1 | `ping 172.22.10.6` (máy in) | 4/4 phản hồi — **được phép** | 3/4 phản hồi, TTL=127; gói đầu mất do ARP | [`20_ACL_Ping_MayIn_DuocPhep`](minh_chung/20_ACL_Ping_MayIn_DuocPhep.png) |
| E3 | PC-HV1 | `ping 172.22.10.5` (máy chủ) | Bị chặn — **chỉ mở DNS/HTTP, không mở ICMP** | `Reply from 172.22.20.1: Destination host unreachable` ×4 (router chặn) | [`21_ACL_Ping_MayChu_BiChan`](minh_chung/21_ACL_Ping_MayChu_BiChan.png) |
| E4 | PC-HV1 | `ping` tới IP hiện tại của PC-GV1 | Bị chặn — **trường hợp bị cấm** | Ping `172.22.10.12`: `Destination host unreachable` ×4 | [`22_ACL_Ping_PC-GV1_BiChan`](minh_chung/22_ACL_Ping_PC-GV1_BiChan.png) |
| E5 | LT-GV2 (Wi-Fi) | `http://portal.minhan.test` | Mở được — ACL áp theo subnet nên laptop cũng theo luật LAN B | Đạt: LT-GV2 mở được portal qua Wi-Fi | [`30_ACL_Web_Wifi_LT-GV2`](minh_chung/30_ACL_Web_Wifi_LT-GV2.png) |
| E6 | PC-GV1 | `ping` tới IP hiện tại của PC-HV1 | 4/4 phản hồi — Giáo vụ **chủ động** liên lạc sang Phòng học được | ❌ **Thất bại**: ping `172.22.20.12` → `Request timed out` ×4. Xem phân tích bên dưới | [`31_ACL_Ping_PC-GV1_PC-HV1_ThatBai`](minh_chung/31_ACL_Ping_PC-GV1_PC-HV1_ThatBai.png) |
| E7 | R-MA (CLI) | `show access-lists` | Số `match` của từng dòng tăng sau các phép thử trên | Dòng 10: 3, dòng 20: 7, dòng 30: 4, dòng 40: **8** (= 4 gói E3 + 4 gói E4), dòng 50: 10 match | [`23_ACL_ShowAccessLists`](minh_chung/23_ACL_ShowAccessLists.png) |
| E8 | SW-PHONGHOC (CLI) | `show port-security interface fa0/1` | `Port Security: Enabled`, `Maximum: 1`, `Violation Mode: Restrict` | Enabled, Secure-up, Maximum 1, Restrict, Violation Count 0; `show port-security address` có 3 MAC SecureSticky trên Fa0/1–3 | [`24_PortSecurity_SW-PHONGHOC`](minh_chung/24_PortSecurity_SW-PHONGHOC.png) |

> **Phân tích phép thử E6 (thất bại).**
> **Hiện tượng:** PC-GV1 ping PC-HV1 nhận `Request timed out`, không phải `Destination host unreachable`.
> **Nguyên nhân:** ACL mở rộng của IOS là **không trạng thái** (stateless), mỗi gói được xét độc lập.
> Gói *echo request* từ Giáo vụ đi **ra** cổng G0/1 nên không bị ACL (đặt chiều `in`) kiểm tra, và tới được PC-HV1.
> Nhưng gói *echo reply* của PC-HV1 đi **vào** G0/1 với nguồn `172.22.20.x`, đích `172.22.10.x`,
> khớp dòng `deny ip 172.22.20.0 0.0.0.63 172.22.10.0 0.0.0.31` nên bị huỷ.
> Vậy mục tiêu "chiều ngược lại không bị giới hạn" ở mục 2 **chưa đạt**: ACL chặn cả phản hồi.
> **Cách xử lý (đã áp dụng vào file ACL):** thêm trước dòng `deny` các luật cho phép gói phản hồi:
> `permit icmp 172.22.20.0 0.0.0.63 172.22.10.0 0.0.0.31 echo-reply` (cho ping từ Giáo vụ)
> và `permit tcp 172.22.20.0 0.0.0.63 172.22.10.0 0.0.0.31 established` (cho phiên TCP do Giáo vụ mở).
> Học viên vẫn không tự mở được kết nối mới sang khu Giáo vụ. Ảnh `31` là lần chạy **trước** khi sửa; cần chạy lại E6 sau khi sửa.

Trước khi chụp E7, nên xoá bộ đếm cho số liệu sạch:

```
clear ip access-list counters
```

## 6. Những gì phần mở rộng này **không** làm

Để trả lời trung thực nếu bị hỏi: ACL này lọc theo địa chỉ và cổng dịch vụ, **không** phải
tường lửa có trạng thái (stateful). Nó không theo dõi phiên kết nối, không kiểm tra nội dung
gói, và không chống được việc một máy ở LAN B tự đặt IP tĩnh thuộc dải LAN A rồi cắm thẳng
vào switch khu Giáo vụ. Port-security giảm bớt rủi ro cắm thiết bị lạ ở khu Phòng học nhưng
cũng chỉ ở mức địa chỉ MAC, vốn có thể giả mạo.

Phần mở rộng cũng chưa gồm NAT/Internet và chưa có chi nhánh thứ hai — đề bài chỉ yêu cầu
chọn một nội dung, không bắt buộc triển khai tất cả.
