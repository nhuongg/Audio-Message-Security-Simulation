import os
import base64
import json
# render_template_string được thay bằng render_template
from flask import Flask, request, jsonify, render_template
from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# --- LOGIC MÁY CHỦ (BACKEND) ---

def generate_key_pair():
    """Tạo cặp khóa RSA và trả về ở định dạng PEM."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    return pem_private, pem_public

def deserialize_keys(pem_private_key, pem_public_key):
    """Chuyển đổi chuỗi PEM thành đối tượng khóa của thư viện cryptography."""
    private_key = serialization.load_pem_private_key(pem_private_key.encode('utf-8'), password=None) if pem_private_key else None
    public_key = serialization.load_pem_public_key(pem_public_key.encode('utf-8')) if pem_public_key else None
    return private_key, public_key

# Route gốc, trả về file index.html từ thư mục templates
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint để tạo khóa cho Alice và Bob
@app.route('/generate-all-keys', methods=['POST'])
def generate_all_keys_api():
    alice_private, alice_public = generate_key_pair()
    bob_private, bob_public = generate_key_pair()
    return jsonify({
        "alice_public_key": alice_public, "alice_private_key": alice_private,
        "bob_public_key": bob_public, "bob_private_key": bob_private
    })

# API endpoint chính để xử lý tin nhắn
@app.route('/process-message', methods=['POST'])
def process_message_api():
    log = []
    try:
        audio_file = request.files.get('audio_data')
        if not audio_file:
            raise ValueError("Không nhận được dữ liệu âm thanh.")

        alice_pem_private = request.form.get('alice_private_key')
        alice_pem_public = request.form.get('alice_public_key')
        bob_pem_public = request.form.get('bob_public_key')
        bob_pem_private = request.form.get('bob_private_key')

        audio_message_bytes = audio_file.read()

        # --- Phía Người gửi (Alice) ---
        log.append("--- Bắt đầu phía Người gửi (Alice) ---")
        alice_private_key, _ = deserialize_keys(alice_pem_private, None)
        _, bob_public_key = deserialize_keys(None, bob_pem_public)

        aes_key = os.urandom(32)
        log.append("1. Alice: Tạo khóa phiên AES-256 ngẫu nhiên.")

        encrypted_aes_key = bob_public_key.encrypt(
            aes_key,
            rsa_padding.OAEP(mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        log.append("2. Alice: Mã hóa khóa AES bằng khóa công khai của Bob.")

        iv = os.urandom(16)
        cipher_aes = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
        padder = PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(audio_message_bytes) + padder.finalize()
        ciphertext = cipher_aes.encryptor().update(padded_data)
        log.append("3. Alice: Mã hóa tin nhắn thoại bằng AES-256 CBC.")

        data_to_hash = iv + ciphertext
        hasher = hashes.Hash(hashes.SHA256())
        hasher.update(data_to_hash)
        final_hash = hasher.finalize()
        log.append(f"4. Alice: Tạo hash SHA-256.")

        signature = alice_private_key.sign(
            final_hash,
            rsa_padding.PSS(mgf=rsa_padding.MGF1(hashes.SHA256()), salt_length=rsa_padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        log.append("5. Alice: Dùng khóa riêng của mình để ký lên hash.")

        packet = {
            "encrypted_aes_key": base64.b64encode(encrypted_aes_key).decode('utf-8'),
            "iv": base64.b64encode(iv).decode('utf-8'),
            "cipher": base64.b64encode(ciphertext).decode('utf-8'),
            "hash": final_hash.hex(),
            "sig": base64.b64encode(signature).decode('utf-8')
        }
        log.append("6. Alice: Đóng gói và gửi đi.")

        # --- Phía Người nhận (Bob) ---
        log.append("\n--- Bắt đầu phía Người nhận (Bob) ---")
        _, alice_public_key = deserialize_keys(None, alice_pem_public)
        bob_private_key_obj, _ = deserialize_keys(bob_pem_private, None)

        decrypted_aes_key = bob_private_key_obj.decrypt(
            base64.b64decode(packet['encrypted_aes_key']),
            rsa_padding.OAEP(mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        log.append("1. Bob: Dùng khóa riêng giải mã thành công khóa AES.")

        log.append("2. Bob: Bắt đầu kiểm tra chữ ký và tính toàn vẹn...")
        recalculated_hash_obj = hashes.Hash(hashes.SHA256())
        recalculated_hash_obj.update(base64.b64decode(packet['iv']) + base64.b64decode(packet['cipher']))
        recalculated_hash = recalculated_hash_obj.finalize()

        if recalculated_hash.hex() != packet['hash']:
            raise ValueError("Lỗi Toàn vẹn (Integrity Error)! Hash không khớp.")
        log.append("   - Kiểm tra Hash Toàn vẹn: OK.")

        alice_public_key.verify(
            base64.b64decode(packet['sig']),
            recalculated_hash,
            rsa_padding.PSS(mgf=rsa_padding.MGF1(hashes.SHA256()), salt_length=rsa_padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        log.append("   - Xác thực Chữ ký của Alice: OK.")

        log.append("3. Bob: Mọi thứ hợp lệ. Tiến hành giải mã tin nhắn thoại...")
        decryptor_cipher = Cipher(algorithms.AES(decrypted_aes_key), modes.CBC(base64.b64decode(packet['iv'])))
        unpadder = PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_padded_msg = decryptor_cipher.decryptor().update(base64.b64decode(packet['cipher']))
        decrypted_msg_bytes = unpadder.update(decrypted_padded_msg) + unpadder.finalize()

        log.append(f"   - Giải mã thành công! Nhận được {len(decrypted_msg_bytes)} bytes dữ liệu âm thanh.")
        log.append(f"\n✅ TIN NHẮN THOẠI ĐÃ ĐƯỢC GIẢI MÃ AN TOÀN! (Gửi ACK)")

        return jsonify({"success": True, "packet": packet, "log": "\n".join(log)})

    except Exception as e:
        log.append(f"\n❌ NACK: ĐÃ XẢY RA LỖI: {str(e)}")
        return jsonify({"success": False, "log": "\n".join(log)})

# Khối này chỉ chạy khi bạn thực thi file trực tiếp (python app.py)
# Gunicorn sẽ không chạy khối này trong môi trường production.
if __name__ == '__main__':
    # Chạy ở chế độ debug để dễ dàng kiểm tra và phát triển.
    app.run(host='0.0.0.0', port=5000, debug=True)