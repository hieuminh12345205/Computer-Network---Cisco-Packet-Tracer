# Hướng dẫn nhanh — làm theo từng bước

Tài liệu nội bộ của nhóm. Mỗi mục bên dưới là **một việc**. Cứ làm lần lượt từng bước,
xong thì so với dòng **"Đúng là khi"** để biết mình làm đúng chưa.

Không cần hiểu hết ngay. Cứ bấm theo, phần giải thích nằm ở dòng **"Hiểu nhanh"**.

---

## Trước khi bắt đầu — nhớ mấy thứ này

| Cái gì | Giá trị |
|---|---|
| Phần mềm | Cisco Packet Tracer **9.0.1** |
| File chính | `CSE3030_MinhAn.pkt` |
| File phần mở rộng (ACL) | `CSE3030_MinhAn_MoRong_ACL.pkt` |
| Trang web nội bộ | `http://portal.minhan.test` |
| Máy chủ web + DNS | `172.22.10.5` |
| Máy in | `172.22.10.6` |
| Tên Wi-Fi | `MINHAN-TEACHER` |
| Mật khẩu Wi-Fi | `MinhAnLab2026!` *(có dấu `!` ở cuối)* |
| Đăng nhập router/switch | `admin` / `MinhAn@Admin26` |
| Mật khẩu `enable` | `MinhAn@Enable26` |

**Trên sơ đồ có 2 khu:**
- **Khu A — Giáo vụ:** các máy tên `PC-GV1`, `PC-GV2`, `PC-GV3`, máy chủ `SRV-PORTAL`, máy in `PRN-GIAOVU`.
- **Khu B — Phòng học:** các máy tên `PC-HV1`, `PC-HV2`, `PC-HV3`, bộ phát Wi-Fi `AP-GIANGVIEN`, hai laptop `LT-GV1`, `LT-GV2`.
- Ở giữa là router **`R-MA`**, nối hai khu lại với nhau.

---

## Feature 1: Mở file và chờ mạng sẵn sàng

**Bước 1:** Mở Packet Tracer.

**Bước 2:** Bấm **File → Open**, chọn file `CSE3030_MinhAn.pkt`.

**Bước 3:** Nhìn góc dưới bên phải màn hình, chắc chắn đang ở chế độ **Realtime** (không phải Simulation).

**Bước 4:** Bấm nút **Fast Forward Time** (hình mũi tên `⏩` ở góc dưới) khoảng 3–4 lần.

**Bước 5:** Nhìn các đường dây nối giữa các máy.

✅ **Đúng là khi:** đầu dây nào cũng có **chấm xanh lá**. Hai laptop có vạch sóng nối tới bộ phát Wi-Fi.

💡 **Hiểu nhanh:** lúc mới mở file, mạng cần vài giây để "khởi động". Nếu thấy chấm **cam** thì cứ bấm Fast Forward thêm, đợi nó chuyển xanh.

---

## Feature 2: Xem một máy đã nhận địa chỉ IP chưa

**Bước 1:** Bấm vào máy `PC-HV1`.

**Bước 2:** Chọn tab **Desktop**.

**Bước 3:** Bấm vào ô **IP Configuration**.

**Bước 4:** Chắc chắn đang chọn ô **DHCP** (ở phía trên).

**Bước 5:** Đọc các dòng hiện ra.

✅ **Đúng là khi:**
- **IPv4 Address** bắt đầu bằng `172.22.20.` (khu B)
- **Default Gateway** là `172.22.20.1`
- **DNS Server** là `172.22.10.5`

**Bước 6:** Làm lại y hệt với `PC-GV1`.

✅ **Đúng là khi:** IP bắt đầu bằng `172.22.10.` (khu A), Gateway là `172.22.10.1`, DNS vẫn là `172.22.10.5`.

💡 **Hiểu nhanh:** máy tính không tự đặt IP, mà **xin** router cấp cho. Việc tự xin này gọi là **DHCP**. Khu A và khu B được cấp hai dải số khác nhau, nên nhìn số IP là biết máy thuộc khu nào.

### 📖 Hiểu kỹ hơn về DHCP (đọc khi có thời gian)

**1. Bốn dòng trong IP Configuration nghĩa là gì?**

Router `R-MA` giống **cô lễ tân phát số phòng**. Mỗi máy cần đủ 4 thông tin mới hoạt động được:

| Ô trong IP Configuration | Ví dụ PC-GV1 (khu A) | Ví dụ PC-HV1 (khu B) | Ý nghĩa đời thường |
|---|---|---|---|
| **IPv4 Address** | `172.22.10.12` | `172.22.20.10` | **Số nhà** của máy. Không máy nào được trùng. |
| **Subnet Mask** | `255.255.255.224` | `255.255.255.192` | **Cỡ khu phố**: khu có bao nhiêu số nhà. |
| **Default Gateway** | `172.22.10.1` | `172.22.20.1` | **Cổng ra khỏi khu**, chính là router. Gửi gì sang khu khác thì đưa cho cổng này. |
| **DNS Server** | `172.22.10.5` | `172.22.10.5` | **Danh bạ**: đổi tên `portal.minhan.test` thành số `172.22.10.5`. |

Không có DHCP thì phải **gõ tay 4 dòng này cho từng máy**, nhiều máy thì dễ gõ nhầm hoặc trùng. Có DHCP, máy chỉ cần chọn **DHCP** là tự nhận đủ.

**2. Máy "xin" IP như thế nào? 4 bước, gọi tắt là DORA**

Vừa bật lên, máy **chưa có số nhà**, nên nó không biết router ở đâu. Nó phải **hét lên với cả khu** (gọi là *broadcast*):

1. **D – Discover:** Máy: *"Có ai phát IP không? Cho tôi một số với!"*
2. **O – Offer:** Router: *"Có đây. Bạn lấy số `172.22.10.12` nhé, kèm mask, gateway, DNS."*
3. **R – Request:** Máy: *"OK, tôi xin lấy số đó."*
4. **A – Acknowledge:** Router: *"Đồng ý, số đó là của bạn."*

Sau đó máy còn hét thêm câu *"Có ai đang dùng `172.22.10.12` không?"* để chắc là không trùng (gói **ARP** có IP nguồn = IP đích).

👉 **Xem tận mắt:** vào Simulation, **Edit Filters** chỉ để **DHCP**. Mở một PC, vào IP Configuration, bấm **Static** rồi bấm lại **DHCP**. Bạn sẽ thấy 4 phong bì DORA chạy qua lại.

**3. Một router mà phát hai loại số. Sao nó biết máy nào ở khu nào?**

Router có **2 cổng**, mỗi cổng nối với một khu:

```
              R-MA (router)
             /            \
   G0/0 = 172.22.10.1    G0/1 = 172.22.20.1
          |                      |
   SW-GIAOVU               SW-PHONGHOC
   (khu A – Giáo vụ)       (khu B – Phòng học)
```

Router đặt sẵn **2 "kho số"** (gọi là *DHCP pool*):

- Kho `GIAOVU` (khu A): phát từ `172.22.10.10` tới `.29`
- Kho `PHONGHOC` (khu B): phát từ `172.22.20.10` tới `.59`

Lời xin của máy **đi vào cổng nào** thì router lấy số ở **kho của cổng đó**:

- PC-GV1 cắm vào SW-GIAOVU, lời xin vào **G0/0**, nên nhận `172.22.10.x`.
- PC-HV1 cắm vào SW-PHONGHOC, lời xin vào **G0/1**, nên nhận `172.22.20.x`.

👉 Máy không tự chọn khu. **Chỗ cắm dây quyết định khu.**

**4. Nhìn số IP là biết khu nào: xem số thứ 3**

| IP có dạng | Thuộc khu | Mask | Số máy dùng được |
|---|---|---|---|
| `172.22.`**`10`**`.x` | Khu A – Giáo vụ (8 người) | `/27` = `255.255.255.224` | 30 |
| `172.22.`**`20`**`.x` | Khu B – Phòng học (22 người) | `/26` = `255.255.255.192` | 62 |

Hai khu **mask khác nhau** vì cần số lượng máy khác nhau. Chọn khu vừa đủ chỗ (còn dư để mở rộng) thì không lãng phí địa chỉ. Đây là ý **chia mạng con (subnetting)** trong đề.

**5. Vì sao DHCP không phát từ `.1`?**

Các số nhỏ được **giữ lại cho thiết bị cố định**, vì những thiết bị này không được đổi số:

| Số | Dùng cho |
|---|---|
| `.1` | Router (cổng ra khỏi khu) |
| `.2` | Switch (để quản lý từ xa) |
| `.5` | Server Portal (DNS + Web), chỉ ở khu A |
| `.6` | Máy in, chỉ ở khu A |
| `.10` trở lên | **DHCP phát cho PC và laptop** |

Số của máy in mà thay đổi lung tung thì mọi người không in được. Vì vậy server, máy in, router phải có **số cố định**, còn PC thì nhận số nào cũng được. Trên router, việc "giữ lại" này là lệnh `ip dhcp excluded-address`.

**🎤 Câu trả lời mẫu khi thầy hỏi về DHCP:**

> "Các máy để ở chế độ DHCP nên tự xin IP từ router R-MA. Router có 2 pool: pool GIAOVU phát 172.22.10.10–29 cho cổng G0/0, pool PHONGHOC phát 172.22.20.10–59 cho cổng G0/1. Máy cắm ở khu nào thì nhận IP của khu đó, kèm mask, gateway và DNS 172.22.10.5. Các địa chỉ thấp được loại trừ để dành cho router, switch, server và máy in."

---

## Feature 3: Kiểm tra hai máy cùng khu nói chuyện được với nhau

**Bước 1:** Làm Feature 2 với **cả hai máy** `PC-GV1` và `PC-GV2`, ghi lại IP của từng máy.

> ⚠️ DHCP phát số theo thứ tự máy nào xin trước, nên **mỗi lần mở file số có thể khác**. Ví dụ một lần chạy: PC-GV1 = `172.22.10.12`, PC-GV2 = `172.22.10.10`. Luôn xem số thật, đừng chép số trong tài liệu.

**Bước 2:** Bấm vào `PC-GV1` → tab **Desktop** → **Command Prompt**.

**Bước 3:** Gõ `ping` + **IP của PC-GV2** (không phải IP của PC-GV1!) rồi Enter. Ví dụ:

```
ping 172.22.10.10
```

> ❗ Gõ nhầm IP của chính PC-GV1 thì máy **ping chính nó**, lúc nào cũng thông, nên không chứng minh được gì.

✅ **Đúng là khi:** hiện 4 dòng `Reply from ...`, dòng cuối ghi **Lost = 0**.

**Bước 4:** Gõ tiếp:

```
ping 172.22.10.1
```

✅ **Đúng là khi:** cũng có 4 dòng `Reply from 172.22.10.1`. Đó là router đang trả lời.

💡 **Hiểu nhanh:** `ping` giống như gọi "Ê, có đó không?" và chờ máy kia trả lời. Có `Reply` là thông. Dòng đầu tiên đôi khi bị mất (`Request timed out`) — bình thường, vì lần đầu máy còn phải đi hỏi đường.

---

## Feature 4: Kiểm tra hai khu nói chuyện được với nhau

**Bước 1:** Bấm vào `PC-HV1` (khu B) → **Desktop** → **Command Prompt**.

**Bước 2:** Gõ lệnh ping sang máy chủ ở khu A:

```
ping 172.22.10.5
```

✅ **Đúng là khi:** có dòng `Reply from 172.22.10.5` với **TTL=127** (bị trừ 1 vì đã đi qua router; ping trong cùng khu thì là 128).

> Lần ping **đầu tiên** sau khi mở file thường có 1 dòng `Request timed out` (Lost = 1). Đó là lúc router đang đi hỏi ARP "máy 172.22.10.5 là ai?", nên gói đầu bị bỏ. Gõ lại lệnh ping lần nữa thì phải ra đủ **4/4 Reply, Lost = 0**. Khi chụp minh chứng, chụp lần thứ hai này.

**Bước 3:** Gõ tiếp lệnh này để xem gói tin đi qua những đâu:

```
tracert 172.22.10.5
```

✅ **Đúng là khi:** hiện **2 dòng**:
1. `172.22.20.1` — đi qua router trước
2. `172.22.10.5` — tới máy chủ

💡 **Hiểu nhanh:** hai khu là hai mạng riêng, muốn nói chuyện phải đi qua router `R-MA` ở giữa. `tracert` cho thấy rõ đúng một lần đi qua router.

---

## Feature 5: Mở trang web nội bộ

**Bước 1:** Bấm vào `PC-GV1` → tab **Desktop** → **Web Browser**.

**Bước 2:** Gõ vào ô địa chỉ:

```
http://portal.minhan.test
```

**Bước 3:** Bấm **Go**.

✅ **Đúng là khi:** hiện trang **"Chao mung den voi Minh An"** có lịch học và thông báo.

**Bước 4:** Làm lại y hệt trên `PC-HV1` (khu B).

✅ **Đúng là khi:** cũng ra đúng trang đó.

**Bước 5 (thêm, để chứng minh DNS chạy):** trên `PC-HV1`, gõ thử `http://172.22.10.5`.

✅ **Đúng là khi:** ra cùng một trang.

💡 **Hiểu nhanh:** máy tính chỉ hiểu số IP, không hiểu chữ `portal.minhan.test`. Máy chủ có một "danh bạ" gọi là **DNS**, tra chữ ra số `172.22.10.5`. Gõ chữ hay gõ số đều ra cùng trang → danh bạ đang hoạt động.

---

## Feature 6: Laptop kết nối Wi-Fi

**Bước 1:** Bấm vào `LT-GV2` (hoặc `LT-GV1`, cấu hình giống nhau) → tab **Desktop** → biểu tượng **PC Wireless** (hình cột ăng-ten, hàng 2, ô đầu tiên).

**Bước 2:** Cửa sổ **Linksys** hiện ra, xem tab **Link Information** (thường mở sẵn).

✅ **Đúng là khi:** ghi **"You have successfully connected to the access point"**, hai vạch **Signal Strength** và **Link Quality** xanh đầy.

**Bước 2b:** Bấm nút **More Information**.

✅ **Đúng là khi:** dòng **Wireless Network Name (SSID)** là **`MINHAN-TEACHER`**, bảo mật **WPA2**.

**Bước 3:** Quay lại **Desktop** → **IP Configuration**.

✅ **Đúng là khi:** IP bắt đầu bằng `172.22.20.` — giống các máy khu B.

**Bước 4:** **Desktop** → **Web Browser** → gõ `http://portal.minhan.test`.

✅ **Đúng là khi:** mở được trang web qua Wi-Fi.

💡 **Hiểu nhanh:** bộ phát Wi-Fi cắm vào switch khu B, nên laptop dùng Wi-Fi cũng được tính là máy khu B. Wi-Fi có mật khẩu kiểu **WPA2**, ai không biết mật khẩu thì không vào được.

**Nếu laptop chưa kết nối:** vào **PC Wireless → Connect** → chọn `MINHAN-TEACHER` → **Connect** → nhập mật khẩu `MinhAnLab2026!`.

---

## Feature 7: Kiểm tra máy in

**Bước 1:** Bấm vào `LT-GV2` → **Desktop** → **Command Prompt**.

**Bước 2:** Gõ:

```
ping 172.22.10.6
```

✅ **Đúng là khi:** có 4 dòng `Reply from 172.22.10.6`, **TTL=127**.

**Bước 3:** Làm lại lệnh ping đó trên `PC-HV1` (khu B, nối dây) và `PC-GV1` (khu A, cùng khu với máy in).

✅ **Đúng là khi:** cả ba máy đều **4/4 Reply, Lost = 0**:

| Ping từ | TTL thấy được | Vì sao |
|---|---|---|
| `PC-GV1` (khu A) | **128** | Cùng khu, không đi qua router |
| `PC-HV1` (khu B) | **127** | Đi qua `R-MA` một lần, bị trừ 1 |
| `LT-GV2` (Wi-Fi) | **127** | Cũng ở khu B, đi qua router một lần |

Laptop Wi-Fi có thời gian (`time=`) lớn hơn máy cắm dây, vài chục ms. Bình thường, sóng Wi-Fi chậm hơn dây.

💡 **Hiểu nhanh:** máy in nằm ở khu A nhưng laptop khu B vẫn với tới được → máy in đúng là **dùng chung**. Đề bài chỉ cần ping được máy in, **không cần in thật**.

---

## Feature 8: Xem gói tin chạy trên sơ đồ (Simulation)

**Bước 1:** Góc dưới bên phải, bấm chuyển từ **Realtime** sang **Simulation**.

**Bước 2:** Trong khung Simulation, bấm **Edit Filters** → chỉ để tích **ICMP** và **ARP**, bỏ tích hết cái khác.

**Bước 3:** Trên **thanh công cụ thứ hai ở phía trên** (hàng có mũi tên chọn, kính lúp, dấu X xoá), nhìn sang **cuối hàng bên phải**: có 2 hình phong bì. Bấm vào **phong bì kín** (cái thứ nhất, tên *Add Simple PDU*, phím tắt `P`). Cái thứ hai là phong bì mở (*Add Complex PDU*), không dùng.

**Bước 4:** Bấm vào `PC-GV1`, rồi bấm vào `PC-HV3`.

**Bước 5:** Bấm nút **Capture / Forward** (`▶|`) từng lần một, nhìn phong bì chạy.

✅ **Đúng là khi:** phong bì chạy theo đường:

```
PC-GV1 → SW-GIAOVU → R-MA → SW-PHONGHOC → PC-HV3
```

rồi chạy ngược về. Cuối cùng khung bên phải ghi **Successful**.

💡 **Hiểu nhanh:** đây là "quay chậm" đường đi của gói tin. Phong bì nào ghi **ARP** là máy đang đi hỏi "ai đang giữ địa chỉ này?" — luôn xảy ra trước khi gửi gói thật.

**Bước 6:** Xong thì bấm lại về **Realtime**.

**Nếu ghi Failed ở lần đầu:** bình thường, nhất là khi vừa mở file. Router phải đi hỏi ARP nên gói đầu bị bỏ. Ở bảng PDU dưới cùng, **bấm đúp vào chấm đỏ ở cột Fire** của dòng đó để gửi lại, rồi bấm ▶ Play. Lần hai phải ra **Successful**.

💡 Khi demo trước thầy: mở file xong, ping vài lệnh ở **Realtime** trước cho mạng "quen nhau", rồi mới chuyển sang Simulation.

⚠️ **Gói ping (PDU) nhớ số IP, không nhớ tên máy.** PDU tạo hôm trước tới một PC dùng DHCP có thể chạy nhầm sang máy khác, vì lần mở file sau IP đã đổi chủ. Vì vậy file chỉ lưu sẵn 2 gói tới IP cố định (server `.5`, máy in `.6`). Gói tới PC thì **mỗi lần demo tạo mới**, và xem Event List để chắc gói tới đúng máy đích.

**Thấy phong bì có dấu ❌ đỏ thì sao?** Dấu X nghĩa là **máy đó bỏ gói tin**, thường **không phải lỗi**:

- Phong bì **ARP** (hoặc DHCP) bị X ở nhiều máy cùng lúc: đó là câu hỏi broadcast gửi cho cả khu, máy nào không phải đích thì bỏ. **Bình thường.**
- Phong bì **ICMP** bị X ở `R-MA` khi đang mở file `..._MoRong_ACL.pkt`: **ACL đang chặn**, đúng thiết kế.
- Phong bì **ICMP** bị X khi đang mở file gốc, và gửi lại lần 2 vẫn X: lúc này **mới là lỗi**, chụp lại cho cả nhóm xem.

Muốn biết chính xác lý do: bấm vào **ô vuông màu** ở cột Info trong Event List (hoặc bấm trúng hình phong bì, đừng bấm vào máy). Cửa sổ **PDU Information** hiện ra, đọc dòng chữ ở tab **OSI Model**.

**Phong bì màu hồng chạy liên tục là gì?** Đó là gói **STP**: switch tự gửi khoảng 2 giây một lần để kiểm tra mạng không bị vòng lặp dây. Bình thường. Muốn sơ đồ gọn khi demo thì bỏ tích **STP** trong Edit Filters.

---

## Feature 9: Đăng nhập vào router

**Bước 1:** Bấm vào router `R-MA` → tab **CLI**.

**Bước 2:** Bấm Enter một cái.

✅ **Đúng là khi:** hiện dòng cảnh báo bắt đầu bằng `Canh bao: Thiet bi mang Trung tam Dao tao Minh An...` và hỏi **Username**.

**Bước 3:** Gõ `admin` → Enter.

**Bước 4:** Gõ mật khẩu `MinhAn@Admin26` → Enter. *(Gõ mật khẩu sẽ không hiện chữ gì — bình thường, cứ gõ rồi Enter.)*

**Bước 5:** Gõ `enable` → Enter.

**Bước 6:** Gõ mật khẩu `MinhAn@Enable26` → Enter.

✅ **Đúng là khi:** dấu nhắc đổi từ `R-MA>` thành **`R-MA#`**.

💡 **Hiểu nhanh:** `>` là quyền xem thường, `#` là quyền quản trị cao nhất. Có mật khẩu để người lạ không vào sửa cấu hình router được. Hai switch đăng nhập y hệt.

---

## Feature 10: Xem router đang làm gì (bảng định tuyến, DHCP)

Làm Feature 9 trước để có dấu `R-MA#`.

**Bước 1:** Gõ:

```
show ip interface brief
```

✅ **Đúng là khi:** dòng `GigabitEthernet0/0` và `GigabitEthernet0/1` đều ghi **up up**.

**Bước 2:** Gõ:

```
show ip route
```

✅ **Đúng là khi:** có 2 dòng bắt đầu bằng chữ **C**: `172.22.10.0/27` và `172.22.20.0/26`.

**Bước 3:** Gõ:

```
show ip dhcp binding
```

✅ **Đúng là khi:** thấy danh sách các máy đã được cấp IP, **không có hai máy trùng số**.

💡 **Hiểu nhanh:** chữ **C** nghĩa là *Connected* — hai khu cắm thẳng vào router nên router tự biết đường, không cần cài thêm gì.

**Mẹo:** nếu màn hình hiện `--More--` thì bấm phím **Space** để xem tiếp.

---

## Feature 11: Demo chặn truy cập (phần mở rộng ACL)

Phần này dùng **file khác**.

**Bước 1:** **File → Open** → chọn `CSE3030_MinhAn_MoRong_ACL.pkt`. Làm lại Feature 1 để chờ mạng sẵn sàng.

**Bước 2:** Bấm `PC-HV1` → **Web Browser** → `http://portal.minhan.test`.

✅ **Đúng là khi:** **mở được** trang web. *(Được phép.)*

**Bước 3:** Bấm `PC-HV1` → **Command Prompt** → gõ:

```
ping 172.22.10.6
```

✅ **Đúng là khi:** có `Reply`. *(Máy in được phép.)*

**Bước 4:** Vẫn trên `PC-HV1`, gõ:

```
ping 172.22.10.5
```

✅ **Đúng là khi:** **không có Reply**, hiện `Destination host unreachable` hoặc `Request timed out`. *(Bị chặn.)*

**Bước 5:** Xem IP của `PC-GV1` (như Feature 2), rồi từ `PC-HV1` ping tới IP đó.

✅ **Đúng là khi:** **bị chặn**, không có Reply.

**Bước 6:** Đăng nhập router `R-MA` (Feature 9), gõ:

```
show access-lists
```

✅ **Đúng là khi:** hiện danh sách **`PHONGHOC-IN`** có 6 dòng, cuối mỗi dòng có số **matches** tăng lên sau các lần thử ở trên.

💡 **Hiểu nhanh:** **ACL** giống bảo vệ đứng ở cửa router, cầm danh sách "ai được đi đâu". Học viên khu B được vào **xem web** và **dùng máy in**, nhưng không được chọc vào máy của giáo vụ. Điểm hay để kể khi demo: **web vào được mà ping máy chủ lại bị chặn** → bảo vệ không chỉ nhìn "đi tới nhà nào", mà còn nhìn "đi làm việc gì".

---

## Feature 12: Kiểm tra khoá cổng switch (port-security)

Vẫn dùng file `CSE3030_MinhAn_MoRong_ACL.pkt`.

**Bước 1:** Bấm vào switch `SW-PHONGHOC` → tab **CLI** → đăng nhập như Feature 9 (dấu nhắc sẽ là `SW-PHONGHOC#`).

**Bước 2:** Gõ:

```
show port-security interface fa0/1
```

✅ **Đúng là khi:**
- `Port Security` : **Enabled**
- `Maximum MAC Addresses` : **1**
- `Violation Mode` : **Restrict**

💡 **Hiểu nhanh:** mỗi ổ cắm mạng ở phòng học chỉ cho **một máy** dùng. Ai rút máy ra cắm thiết bị lạ vào thì bị chặn. Riêng ổ cắm của bộ phát Wi-Fi thì **không khoá**, vì nhiều laptop cùng đi qua ổ đó.

---

## Feature 13: Chụp ảnh minh chứng

**Bước 1:** Làm xong một Feature, để nguyên cửa sổ đang hiện kết quả đúng.

**Bước 2:** Bấm **Windows + Shift + S** (Windows) hoặc **Cmd + Shift + 4** (Mac), kéo khung chụp vùng có kết quả.

**Bước 3:** Lưu vào thư mục `minh_chung/`, đặt tên theo số tiếp theo, ví dụ:
- `10_ACL_Web_DuocPhep.png`
- `11_ACL_Ping_BiChan.png`
- `12_ACL_ShowAccessLists.png`

**Bước 4:** Mở file `BANG_KIEM_THU.md`, tìm dòng tương ứng, thay chữ *(cần chụp)* bằng kết quả bạn thấy, và ghi tên file ảnh vào cột Minh chứng.

💡 **Mẹo:** chụp sao cho thấy được **tên máy** (ở thanh tiêu đề cửa sổ) và **kết quả**. Thiếu tên máy thì người chấm không biết đang thử trên máy nào.

---

## Khi bị lỗi thì làm gì?

| Bị gì | Làm gì |
|---|---|
| Ping lần đầu báo `Request timed out` | Bình thường. Ping lại lần nữa. |
| Simulation báo **Failed** | Về Realtime, bấm Fast Forward vài lần, thử lại. |
| PC không có IP (toàn số `0` hoặc `169.254...`) | Vào IP Configuration, bấm chọn **Static** rồi bấm lại **DHCP**. |
| Web báo không tìm thấy trang | Xem DNS trong IP Configuration có đúng `172.22.10.5` không. Thử gõ `http://172.22.10.5`. |
| Laptop không có Wi-Fi | Nhập lại mật khẩu `MinhAnLab2026!` — nhớ dấu `!` ở cuối. |
| Vào CLI bị hỏi Username | Đúng rồi đó. Gõ `admin` / `MinhAn@Admin26`. |
| Ping `172.22.10.5` bị chặn | Bạn đang mở **file ACL**. Trong file ACL bị chặn là **đúng**. Muốn ping được thì mở file `CSE3030_MinhAn.pkt`. |
| Lỡ tay sửa lung tung | **Đừng bấm Save.** Đóng file, chọn **No** khi được hỏi lưu, rồi mở lại. |

---

## Thứ tự demo trước giảng viên (gợi ý)

Đi lần lượt, khoảng 10 phút:

1. Feature 1 — mở file
2. Feature 2 — cấp IP
3. Feature 3 — cùng khu
4. Feature 4 — khác khu
5. Feature 5 — trang web
6. Feature 6 + 7 — Wi-Fi và máy in
7. Feature 8 — xem gói tin chạy
8. Feature 10 — router (`show ip route`)
9. Feature 11 — phần mở rộng ACL

Câu trả lời cho các câu hỏi giảng viên hay hỏi nằm trong [`HUONG_DAN_SU_DUNG_VA_DEMO.md`](HUONG_DAN_SU_DUNG_VA_DEMO.md), mục 5.
