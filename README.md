# Mô phỏng Bảo mật Tin nhắn Âm thanh (Secure Audio Messaging Simulation)

[](https://www.python.org/) [](https://flask.palletsprojects.com/) [](https://cryptography.io/) [\![Ngrok](https://img.shields.io/badge/Ngrok- tunnelling-green.svg)](https://ngrok.com/)

Một ứng dụng web tương tác được xây dựng bằng Flask và JavaScript để mô phỏng trực quan quá trình gửi và nhận một tin nhắn âm thanh được bảo mật đầu cuối. Dự án này minh họa các khái niệm mật mã hiện đại như mã hóa hybrid, chữ ký số và xác thực tính toàn vẹn.

Tất cả được gói gọn trong một file Google Colab duy nhất, cho phép bạn chạy và thử nghiệm mà không cần cài đặt môi trường phức tạp trên máy tính cá nhân.

## ✨ Các tính năng chính

  * **Ghi âm trực tiếp từ trình duyệt**: Sử dụng `Web Audio API` để ghi âm giọng nói của bạn làm tin nhắn đầu vào.
  * **Mô phỏng hai phía (Sender & Receiver)**: Giao diện trực quan cho cả "Alice" (Người gửi) và "Bob" (Người nhận) trên cùng một trang.
  * **Mã hóa Hybrid (Hybrid Encryption)**:
      * **AES-256 (CBC)**: Dùng để mã hóa dữ liệu âm thanh (nội dung tin nhắn). AES là một thuật toán mã hóa đối xứng hiệu quả cho dữ liệu lớn.
      * **RSA-2048 (OAEP)**: Dùng để mã hóa khóa AES. RSA là một thuật toán mã hóa bất đối xứng mạnh, đảm bảo chỉ người nhận có khóa riêng tư mới có thể giải mã được khóa phiên AES.
  * **Đảm bảo Tính toàn vẹn & Xác thực (Integrity & Authenticity)**:
      * **SHA-256**: Tạo một bản hash (băm) của tin nhắn đã mã hóa để đảm bảo nó không bị thay đổi trên đường truyền.
      * **Chữ ký số RSA-PSS**: Người gửi (Alice) ký lên hash bằng khóa riêng tư của mình. Người nhận (Bob) có thể xác thực chữ ký này bằng khóa công khai của Alice, đảm bảo tin nhắn thực sự đến từ Alice và không thể bị chối bỏ.
  * **Giao diện web tương tác**: Dễ dàng tạo cặp khóa mới, bắt đầu/dừng ghi âm, và xem kết quả ngay lập tức.
  * **Nhật ký chi tiết (Verbose Log)**: Hiển thị từng bước của quá trình mã hóa và giải mã, giúp người dùng hiểu rõ luồng hoạt động bên dưới.

## ⚙️ Công nghệ sử dụng

  * **Backend**: Python, Flask
  * **Frontend**: HTML5, CSS3, JavaScript (không có framework)
  * **Thư viện Mật mã**: `cryptography` (Python)
  * **Tunneling**: `pyngrok` để tạo một URL công khai cho ứng dụng Flask chạy trên Colab.

## 🚀 Luồng hoạt động mật mã

Ứng dụng mô phỏng một quy trình bảo mật hoàn chỉnh khi Alice gửi tin nhắn thoại cho Bob.

### Phía Người gửi (Alice)

1.  🎙️ **Ghi âm**: Alice ghi âm một tin nhắn thoại.
2.  🔑 **Tạo khóa phiên**: Alice tạo một khóa đối xứng `AES-256` ngẫu nhiên và duy nhất cho tin nhắn này.
3.  🔒 **Mã hóa tin nhắn**: Alice mã hóa tin nhắn thoại bằng khóa `AES` vừa tạo.
4.  📦 **Mã hóa khóa phiên**: Alice mã hóa khóa `AES` bằng **khóa công khai** của Bob (sử dụng `RSA-2048`). Chỉ Bob mới có thể giải mã nó bằng khóa riêng tư của mình.
5.  🧮 **Tạo hash**: Alice tạo một bản băm `SHA-256` từ dữ liệu âm thanh đã mã hóa.
6.  ✍️ **Tạo chữ ký số**: Alice ký lên bản băm này bằng **khóa riêng tư** của mình (sử dụng `RSA-PSS`).
7.  ✉️ **Gửi gói tin**: Alice đóng gói tất cả các thành phần (tin nhắn đã mã hóa, khóa AES đã mã hóa, IV, hash, chữ ký) và gửi cho Bob.

### Phía Người nhận (Bob)

1.  🔑 **Giải mã khóa phiên**: Bob sử dụng **khóa riêng tư** của mình để giải mã khóa `AES`.
2.  ✅ **Xác thực**: Bob thực hiện hai bước kiểm tra quan trọng:
      * **Kiểm tra tính toàn vẹn**: Bob tự tính toán lại hash `SHA-256` từ dữ liệu âm thanh mã hóa nhận được và so sánh với hash mà Alice đã gửi. Nếu khớp, tin nhắn không bị sửa đổi.
      * **Xác thực chữ ký**: Bob sử dụng **khóa công khai** của Alice để xác thực chữ ký. Nếu hợp lệ, điều này chứng tỏ tin nhắn thực sự do Alice gửi.
3.  🔓 **Giải mã tin nhắn**: Nếu cả hai bước xác thực trên đều thành công, Bob sử dụng khóa `AES` đã giải mã để giải mã tin nhắn thoại và nghe nội dung.
4.  ❌ **Từ chối**: Nếu có bất kỳ bước nào thất bại, Bob sẽ hủy bỏ quá trình và coi như tin nhắn không hợp lệ.

## ▶️ Cách chạy dự án

Dự án này được thiết kế để chạy trực tiếp trên **Google Colab**.

1.  **Lấy Ngrok Authtoken**:

      * Truy cập [Ngrok Dashboard](https://dashboard.ngrok.com/get-started/your-authtoken).
      * Đăng ký/đăng nhập và sao chép Authtoken của bạn.

2.  **Mở Notebook và Chạy**:

      * Mở file `Mô_phỏng_Bảo_mật_Tin_nhắn_Âm_thanh.ipynb` bằng Google Colab.
      * Tìm đến dòng code sau:
        ```python
        !ngrok authtoken YOUR_AUTHTOKEN_HERE
        ```
      * Thay thế `YOUR_AUTHTOKEN_HERE` bằng token bạn vừa sao chép.
      * Chạy toàn bộ cell code bằng cách nhấn nút "Play" (▶️) hoặc nhấn `Ctrl + Enter`.

3.  **Truy cập ứng dụng**:

      * Đợi vài giây để các thư viện được cài đặt và máy chủ khởi động.
      * Kết quả output sẽ hiển thị một URL công khai do `ngrok` tạo ra.
        ```
        🌍 Ứng dụng của bạn đang chạy tại URL công khai: https://xxxxxxxx.ngrok-free.app
        ```
      * Nhấp vào URL này để mở ứng dụng trong một tab mới của trình duyệt.

## 📋 Hướng dẫn sử dụng giao diện

1.  **Cấp quyền Micro**: Khi trang web mở ra, trình duyệt có thể sẽ hỏi bạn quyền truy cập micro. Hãy chọn **"Allow" (Cho phép)**.
2.  **Tạo khóa**: Nhấn nút **"Tạo Khóa cho cả Alice và Bob"**. Các khóa RSA sẽ được tạo và điền vào các ô tương ứng.
3.  **Ghi âm**:
      * Nhấn nút **"Bắt đầu Ghi âm"**.
      * Nói vào micro của bạn.
      * Nhấn nút **"Dừng Ghi âm"** khi hoàn tất.
4.  **Xem kết quả**:
      * Ngay sau khi dừng ghi âm, ứng dụng sẽ tự động thực hiện toàn bộ quy trình mật mã.
      * **Nghe lại**: Một trình phát âm thanh sẽ xuất hiện, cho phép bạn nghe lại bản ghi gốc.
      * **Gói tin được gửi đi**: Ô này hiển thị dữ liệu JSON đã được mã hóa và đóng gói, sẵn sàng để "gửi đi".
      * **Nhật ký xử lý**: Ô này hiển thị chi tiết từng bước mà cả Alice và Bob đã thực hiện.

  
*Lưu ý: Thay thế `https://i.imgur.com/example.png` bằng link đến ảnh chụp màn hình thực tế của bạn.*
