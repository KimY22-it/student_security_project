from db.connect_db import get_connection
from encryption import encrypt, generate_data_key, derive_wrapping_key, encrypt_data_key, decrypt_data_key
from validation import validate_registration_input
from hashlib import pbkdf2_hmac
from hmac import compare_digest
import os

def hash_password(password, salt, workload=100000):
    stretched = pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        workload,
    )   
    return stretched.hex()

def verify_password(password, salt, stored_hash, workload=100000):
    computed_hash = hash_password(password, salt, workload)
    return compare_digest(computed_hash, stored_hash)

def register_user(username, password, fullname, gender, email, cccd, phone):
    conn = get_connection()
    if conn is None:
        return False, "Không thể kết nối đến cơ sở dữ liệu."

    cursor = conn.cursor()
    try:
        is_valid, message = validate_registration_input(
            username,
            password,
            fullname,
            email,
            cccd, 
            phone
        )
        if not is_valid:
            return False, message
        if gender not in ["Nam", "Nữ", "Khác"]:
            return False, "Giới tính không hợp lệ."
        
        # Kiểm tra username trùng lặp
        cursor.execute("SELECT id FROM accounts WHERE username = %s", (username,))
        if cursor.fetchone():
            return False, "Tên đăng nhập đã tồn tại."

        # Tạo salt và mã băm mật khẩu
        salt = os.urandom(16).hex()
        pw_hash = hash_password(password, salt)

        # Sinh data_key ngẫu nhiên cho user
        data_key = generate_data_key()   # 16 bytes random

        # Derive wrapping_key từ password + salt (PBKDF2)
        wrapping_key = derive_wrapping_key(password, salt)

        # Mã hóa data_key bằng wrapping_key → lưu DB
        data_key_enc = encrypt_data_key(data_key, wrapping_key)

        # Thêm vào bảng accounts (mặc định role là user)
        cursor.execute(
            "INSERT INTO accounts (username, password_hash, salt, data_key_user_encrypt, role) VALUES (%s, %s, %s, %s, %s)",
            (username, pw_hash, salt, data_key_enc, "user")
        )
        account_id = cursor.lastrowid

        # Mã hóa thông tin cá nhân bằng data_key
        email_enc = encrypt(email, data_key)
        cccd_enc  = encrypt(cccd,  data_key)
        phone_enc = encrypt(phone, data_key)

        # Thêm vào bảng personal_information
        cursor.execute(
            """INSERT INTO personal_information 
               (account_id, fullname, gender, email_encrypt, cccd_encrypt, phone_encrypt) 
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (account_id, fullname, gender, email_enc, cccd_enc, phone_enc)
        )
        
        conn.commit()
        return True, "Đăng ký thành công."
    except Exception as e:
        conn.rollback()
        return False, f"Lỗi hệ thống khi đăng ký: {str(e)}"
    finally:
        cursor.close()
        conn.close()

def check_login(username, password):
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    sql = "SELECT id, username, password_hash, salt, data_key_user_encrypt, role FROM accounts WHERE username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None:
        return None

    account_id        = result[0]
    db_username       = result[1]
    db_password_hash  = result[2]
    db_salt           = result[3]
    db_data_key_enc   = result[4]
    db_role           = result[5]

    if not verify_password(password, db_salt, db_password_hash):    
        return None

    # Admin không cần data_key (chỉ xem bản mã, không giải mã dữ liệu cá nhân)
    if db_role == "admin":
        return {
            "id":       account_id,
            "username": db_username,
            "role":     db_role,
            "data_key": None,
        }

    # User thường: unwrap data_key từ password + salt
    wrapping_key = derive_wrapping_key(password, db_salt)
    data_key     = decrypt_data_key(db_data_key_enc, wrapping_key)

    return {
        "id":       account_id,
        "username": db_username,
        "role":     db_role,
        "data_key": data_key,
    }
