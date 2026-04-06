import re

def is_digits(text):
    if text == "":
        return False
    return text.isdigit()

def is_valid_username(username):
    # Độ dài 3-20, chỉ chữ cái, số và dấu gạch dưới
    if not (3 <= len(username) <= 20):
        return False
    return bool(re.match(r"^[a-zA-Z0-9_]+$", username))

def is_valid_password(password):
    # Tối thiểu 8 ký tự, ít nhất 1 hoa, 1 thường, 1 số
    if len(password) < 6:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True

def is_valid_fullname(fullname):
    # Chỉ chữ cái (bao gồm tiếng Việt) và khoảng trắng, min 2 ký tự
    if len(fullname.strip()) < 2:
        return False
    for ch in fullname:
        if not (ch.isalpha() or ch.isspace()):
            return False
    return True

def is_valid_email(email):
    email = email.strip()
    # Sử dụng regex chuẩn hơn cho email
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(regex, email))

def is_valid_phone(phone):
    phone = phone.strip()
    if len(phone) != 10:
        return False
    return phone.isdigit()

def is_valid_cccd(cccd):
    cccd = cccd.strip()
    if len(cccd) != 12:
        return False
    return cccd.isdigit()

def validate_registration_input(username, password, fullname, email, cccd, phone):
    if not is_valid_username(username):
        return False, "Tên đăng nhập không hợp lệ (3-20 ký tự, chỉ chữ cái, số và '_')."

    if not is_valid_password(password):
        return False, "Mật khẩu không hợp lệ (tối thiểu 6 ký tự, cần có chữ hoa, thường, số)."

    if not is_valid_fullname(fullname):
        return False, "Họ tên không hợp lệ (chỉ chứa chữ cái và khoảng trắng)."

    if not is_valid_email(email):
        return False, "Email không đúng định dạng."

    if not is_valid_phone(phone):
        return False, "Số điện thoại không đúng (phải có 10 chữ số và bắt đầu bằng 0)."

    if not is_valid_cccd(cccd):
        return False, "CCCD không đúng (phải có đúng 12 chữ số)."

    return True, "Hợp lệ."

