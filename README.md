# Mô phỏng Bảo mật Tin nhắn Âm thanh

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask)
![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render)

Một ứng dụng web tương tác để mô phỏng trực quan quá trình gửi và nhận một tin nhắn âm thanh được bảo mật đầu cuối, minh họa các khái niệm mật mã hiện đại như mã hóa hybrid, chữ ký số và xác thực tính toàn vẹn.

[**▶️ Chạy thử ứng dụng tại đây!**](https://audio-message-security-simulation.onrender.com/)

---

## Giao diện ứng dụng
<p align="center">
  <img src="Picture/Screenshot (99).png" alt="Ảnh giao diện chính" width="80%">
</p>
<p align="center">
  <img src="Picture/Screenshot (100).png" alt="Ảnh kết quả xử lý" width="80%">
</p>

*Lưu ý: Bạn cần đảm bảo các file ảnh này nằm trong thư mục `Picture/` trong repository của mình.*

---

## ✨ Các tính năng chính

* **Ghi âm trực tiếp từ trình duyệt**: Sử dụng `Web Audio API` để ghi âm giọng nói của bạn làm tin nhắn đầu vào.
* **Mô phỏng hai phía (Sender & Receiver)**: Giao diện trực quan cho cả "Alice" (Người gửi) và "Bob" (Người nhận) trên cùng một trang.
* **Mã hóa Hybrid (Hybrid Encryption)**:
    * **AES-256 (CBC)**: Dùng để mã hóa dữ liệu âm thanh.
    * **RSA-2048 (OAEP)**: Dùng để mã hóa khóa phiên AES, đảm bảo chỉ người nhận có khóa riêng tư mới có thể giải mã được.
* **Đảm bảo Tính toàn vẹn & Xác thực (Integrity & Authenticity)**:
    * **SHA-256**: Tạo một bản hash (băm) của tin nhắn đã mã hóa để đảm bảo nó không bị thay đổi.
    * **Chữ ký số RSA-PSS**: Người gửi ký lên hash bằng khóa riêng tư, giúp người nhận xác thực nguồn gốc và chống chối bỏ.
* **Giao diện web tương tác**: Dễ dàng tạo cặp khóa mới, ghi âm, và xem kết quả tức thì.
* **Nhật ký chi tiết (Verbose Log)**: Hiển thị từng bước của quá trình mã hóa và giải mã, giúp người dùng hiểu rõ luồng hoạt động bên dưới.

---

## ⚙️ Công nghệ sử dụng

| Phần        | Công nghệ                                                |
| :---------- | :------------------------------------------------------- |
| **Backend** | Python, Flask, Gunicorn                                  |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla JS)                     |
| **Mật mã** | Thư viện `cryptography` của Python                      |
| **Deployment**| Render                                                   |

---

## 🚀 Luồng hoạt động mật mã

Ứng dụng mô phỏng một quy trình bảo mật hoàn chỉnh khi Alice gửi tin nhắn thoại cho Bob.

### Phía Người gửi (Alice)
1.  🎙️ **Ghi âm**: Alice ghi âm một tin nhắn thoại.
2.  🔑 **Tạo khóa phiên**: Alice tạo một khóa đối xứng `AES-256` ngẫu nhiên.
3.  🔒 **Mã hóa tin nhắn**: Alice mã hóa tin nhắn thoại bằng khóa `AES` vừa tạo.
4.  📦 **Mã hóa khóa phiên**: Alice mã hóa khóa `AES` bằng **khóa công khai** của Bob (sử dụng `RSA-2048`).
5.  🧮 **Tạo hash**: Alice tạo một bản băm `SHA-256` từ dữ liệu âm thanh đã mã hóa.
6.  ✍️ **Tạo chữ ký số**: Alice ký lên bản băm bằng **khóa riêng tư** của mình.
7.  ✉️ **Gửi gói tin**: Alice đóng gói tất cả các thành phần và gửi cho Bob.

### Phía Người nhận (Bob)
1.  🔑 **Giải mã khóa phiên**: Bob sử dụng **khóa riêng tư** của mình để giải mã khóa `AES`.
2.  ✅ **Xác thực**:
    * **Kiểm tra tính toàn vẹn**: Bob tự tính toán lại hash `SHA-256` và so sánh với hash nhận được.
    * **Xác thực chữ ký**: Bob sử dụng **khóa công khai** của Alice để xác thực chữ ký.
3.  🔓 **Giải mã tin nhắn**: Nếu xác thực thành công, Bob dùng khóa `AES` để giải mã tin nhắn thoại.
4.  ❌ **Từ chối**: Nếu có bất kỳ bước nào thất bại, Bob sẽ hủy bỏ quá trình.

---

## 💻 Cài đặt và Chạy trên máy cục bộ (Local Development)

Để chạy dự án này trên máy tính của bạn, hãy làm theo các bước sau:

**1. Clone repository:**
```bash
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name
