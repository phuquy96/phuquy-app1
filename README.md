# 🚀 TEST PHUQUY - HỆ THỐNG XÁC THỰC BẢN QUYỀN KEY IOS 26 (SEVER PHUQUY)

Dự án iOS IPA hoàn chỉnh với giao diện **Glassmorphism iOS 26**, tích hợp đầy đủ mã nguồn xác thực máy chủ **PHUQUY SEVER**, kiểm tra phần cứng thiết bị (HWID Lock), Realtime Heartbeat và tự động kick tức thì khi Key hết hạn, bị band, bị xóa hoặc reset từ máy chủ.

---

## 🌟 TÍNH NĂNG NỔI BẬT

1. **Giao Diện Kính Mờ iOS 26 (Glassmorphism):**
   - Nền hình ảnh Shop (`logo.png`) làm mờ sâu kết hợp hiệu ứng Dark Glass & ánh sáng Ambient Neon Glow.
   - Thẻ nhập Key thiết kế bo cong góc mượt mà (Corner Radius 28pt) với viền kính phản chiếu ánh sáng.
   - Không bị tràn viền, tràn chữ hay che nút trên bất kỳ màn hình iPhone nào (tương thích từ iPhone SE đến iPhone 16 Pro Max, iPad).

2. **Logo & Đổi Ngôn Ngữ Thời Gian Thực (VN / EN):**
   - **Logo Shop**: Nằm chính giữa trên cùng của bảng nhập Key.
   - **Nút Ngôn Ngữ**: Nằm tại góc trên cùng bên phải bảng nhập Key:
     - 🇻🇳 **VIETNAM**: Toàn bộ giao diện chuyển sang Tiếng Việt.
     - 🇬🇧 **ENGLISH**: Toàn bộ giao diện chuyển sang Tiếng Anh.

3. **Ô Nhập Key + Nút Dán Tiện Lợi:**
   - Ô nhập Key dạng kính mờ hỗ trợ xóa nhanh, tắt tự động sửa chính tả.
   - Nút **📋 Dán (Paste)** đặt ngay sát cạnh ô nhập Key, chạm 1 chạm để dán ngay mã Key từ bộ nhớ tạm cùng hiệu ứng rung Haptic.

4. **Bảng Thông Báo Thành Công Ô Vuông Bo Góc iOS 26:**
   - Xuất hiện giữa màn hình, làm mờ tối toàn bộ giao diện xung quanh.
   - **Nút tích tròn (✓) phát sáng màu xanh lá** nằm chính giữa trên cùng của bảng vuông.
   - Hiển thị đầy đủ 3 trường thông tin:
     - 🔑 **KEY**: Hiển thị chính xác mã Key khách vừa nhập.
     - ⏳ **THỜI HẠN**: Thời hạn gói Key (ví dụ: `1 Ngày`, `7 Ngày`, `30 Ngày`, `Vĩnh Viễn`).
     - 📅 **HẾT HẠN**: Ngày giờ phút giây cụ thể (`DD/MM/YYYY HH:mm:ss`).
   - Thanh tiến trình đếm ngược **5 giây** và tự động chuyển vào giao diện chính (hoặc bấm **Vào Ngay** để vào lập tức).

5. **Giao Diện Chính & Nút Bật Kiểu iOS 26:**
   - **Nút Bật kiểu iOS 26**: Công tắc chuyển đổi Neon Toggle Switch (Bật / Tắt Mod Menu) mượt mà với âm thanh và rung haptic.
   - Badge trạng thái: `● HOẠT ĐỘNG (ACTIVE)` và thông tin khóa cứng phần cứng thiết bị (`HWID`).
   - Nút **Đổi Key / Đăng Xuất**.

6. **Bảo Mật Máy Chủ & Realtime Heartbeat (severphuquy.sbs):**
   - Tự động lấy UUID duy nhất của thiết bị và khóa cứng Key với thiết bị đó (thiết bị khác không thể dùng chung).
   - Tự động lưu Key vào bộ nhớ máy (`NSUserDefaults`), mở app lần sau sẽ tự động vào thẳng giao diện nếu Key còn hợp lệ.
   - **Đồng bộ thời gian thực (Realtime Heartbeat)**: Cứ mỗi 10 giây gọi API kiểm tra trạng thái Key.
   - **Tự động Kick lập tức**: Nếu trên máy chủ đổi trạng thái Key thành Hết Hạn, Bị Band, Bị Xóa, hoặc Reset:
     - Lập tức đóng Menu (`TeardownModMenu()`).
     - Đưa người dùng về màn hình nhập Key kèm bảng thông báo lỗi màu đỏ:
       - `Key Đã Hết Hạn`
       - `Key Đã Bị Band`
       - `Key Đã Bị Xóa`
       - `Key Không Tồn Tại`

---

## 📁 CẤU TRÚC DỰ ÁN

```
TEST_PHUQUY/
├── .github/workflows/
│   └── build.yml               # File YML build IPA tự động qua GitHub Actions
├── TEST_PHUQUY/
│   ├── PhuQuyAuth.h            # Header chuẩn kết nối máy chủ PHUQUY
│   ├── PhuQuyAuth.m            # Mã xử lý API, HWID, Heartbeat, Kick realtime
│   ├── KeyViewController.h     # Giao diện bảng nhập Key Glass iOS 26
│   ├── KeyViewController.m     # Xử lý nhập Key, Nút Dán, Đổi ngôn ngữ, Modal 5s
│   ├── MainViewController.h    # Giao diện chính sau khi kích hoạt Key
│   ├── MainViewController.m    # Nút Bật kiểu iOS 26, Realtime Heartbeat Listener
│   ├── AppDelegate.h / .m      # Vòng đời ứng dụng & nạp cấu hình máy chủ
│   ├── SceneDelegate.h / .m    # Hỗ trợ iOS 13+
│   ├── main.m                  # Điểm khởi chạy
│   ├── Info.plist              # Cấu hình App: Tên "TEST PHUQUY", Bundle ID
│   └── Assets.xcassets/        # Biểu tượng AppIcon các kích thước và Logo shop
├── TEST_PHUQUY.xcodeproj/      # Dự án Xcode hoàn chỉnh
├── Payload/                    # Thư mục chứa TEST PHUQUY.app
├── dcukey.ipa                  # File IPA đóng gói sẵn
├── dcukey.zip                  # Toàn bộ mã nguồn nén lại để tải và up lên GitHub
├── index.html                  # Trình mô phỏng Web iOS 26 trực quan test ngay trên trình duyệt
└── README.md                   # Hướng dẫn chi tiết
```

---

## 🛠️ HƯỚNG DẪN BUILD FILE IPA TRÊN GITHUB (BẰNG FILE .YML)

Dự án đã có sẵn file workflow `.github/workflows/build.yml`. Bạn chỉ cần thực hiện 3 bước sau:

1. **Tạo Repository mới trên GitHub**:
   - Vào [github.com/new](https://github.com/new) -> Đặt tên (ví dụ: `TEST_PHUQUY`).

2. **Tải file `dcukey.zip` lên Repository**:
   - Giải nén `dcukey.zip` và đẩy code lên GitHub qua Git:
     ```bash
     git init
     git add .
     git commit -m "Khoi tao du an TEST PHUQUY iOS 26"
     git branch -M main
     git remote add origin https://github.com/TEN_GITHUB/TEST_PHUQUY.git
     git push -u origin main
     ```
   - Hoặc bạn có thể tải các thư mục `.github`, `TEST_PHUQUY`, `TEST_PHUQUY.xcodeproj` trực tiếp lên web GitHub.

3. **Tự động nhận file IPA**:
   - Ngay khi bạn đẩy code lên, thẻ **Actions** trên GitHub sẽ tự động chạy máy Mac ảo (macOS 14 với Xcode 15) để biên dịch toàn bộ mã nguồn thành file `dcukey.ipa`.
   - Sau khi hoàn thành (khoảng 1 - 2 phút), bạn vào mục **Actions** hoặc mục **Releases** trên GitHub để tải trực tiếp file `dcukey.ipa` về máy!

---

## 📲 HƯỚNG DẪN CÀI ĐẶT FILE `dcukey.ipa` VÀO IPHONE

Bạn có thể cài đặt trực tiếp file `dcukey.ipa` đã được đóng gói sẵn vào iPhone qua các công cụ phổ biến:

1. **Cài qua Scarlet / ESign / GBox (Không cần máy tính)**:
   - Mở ứng dụng Scarlet hoặc ESign trên iPhone.
   - Nhấn nút Import (nhập) và chọn file `dcukey.ipa`.
   - Ký bằng chứng chỉ (Certificate) của bạn và bấm **Cài Đặt**.

2. **Cài qua TrollStore (Dành cho máy đã cài TrollStore)**:
   - Chia sẻ file `dcukey.ipa` vào TrollStore -> Bấm **Install** (Vĩnh viễn không sợ thu hồi chứng chỉ).

3. **Cài qua AltStore / Sideloadly (Dùng máy tính PC / Mac)**:
   - Mở Sideloadly trên máy tính -> Kết nối iPhone bằng cáp USB.
   - Kéo file `dcukey.ipa` vào Sideloadly -> Nhập Apple ID -> Bấm **Start**.

---

## 🌐 XEM TRƯỚC GIAO DIỆN TRỰC QUAN (WEB SIMULATOR)

Bạn có thể mở file `index.html` bằng bất kỳ trình duyệt nào (Chrome, Safari, Edge trên điện thoại hoặc máy tính) để kiểm tra giao diện trước:
- Bấm nút chọn ngôn ngữ 🇻🇳 / 🇬🇧.
- Thử nút Dán (Paste) từ bộ nhớ tạm.
- Thử các phím bấm test nhanh: Key Hợp Lệ, Key Hết Hạn, Key Bị Band, Key Bị Xóa.
- Xem hiệu ứng đếm ngược 5 giây của ô vuông thành công Glass iOS 26.
- Bật / Tắt nút gạt kiểu iOS 26.
- Bấm nút thử nghiệm Kick từ xa để xem cách app đẩy về màn hình nhập Key.

---

## ⚙️ CẤU HÌNH KẾT NỐI MÁY CHỦ KEY PHUQUY

- **Địa chỉ Máy Chủ**: `https://severphuquy.sbs`
- **Địa chỉ API Key**: `https://severphuquy.sbs/api/server_key.php`
- **Mã Nhận Diện Ứng Dụng (Token)**: `PQ-LIVE-1-F115E83639653E38`

### Tham số gửi lên API:
```http
POST /api/server_key.php HTTP/1.1
Host: severphuquy.sbs
Content-Type: application/x-www-form-urlencoded

token=PQ-LIVE-1-F115E83639653E38&key=PQ-XXXX-XXXX&hwid=UUID-MAY&action=verify
```

### Định dạng phản hồi JSON từ Server:
```json
{
  "status": "success",
  "duration": "1 Ngày",
  "expire_time": "27/09/2026 20:00:00",
  "message": "Key hợp lệ!"
}
```
Khi key bị khóa/hết hạn:
```json
{
  "status": "expired",
  "message": "Key Đã Hết Hạn"
}
```
*(Nếu là `banned` -> thông báo "Key Đã Bị Band"; nếu là `deleted` -> "Key Đã Bị Xóa"; nếu `not_found` -> "Key Không Tồn Tại").*
