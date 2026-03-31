def is_digits(text):
    if text == "":
        return False

    for ch in text:
        if ch < "0" or ch > "9":
            return False
    return True


def is_valid_email(email):
    email = email.strip()

    if '@' not in email:
        return False

    parts = email.split('@')
    if len(parts) != 2:
        return False

    name_part, domain_part = parts

    if len(name_part) == 0 or len(domain_part) == 0:
        return False

    if '.' not in domain_part:
        return False

    if domain_part[0] == '.' or domain_part[-1] == '.':
        return False

    if '..' in email:
        return False

    return True

def is_valid_phone(phone):
    if len(phone) != 10:
        return False
    if not is_digits(phone):
        return False
    return True


def is_valid_cccd(cccd):
    if len(cccd) != 12:
        return False
    if not is_digits(cccd):
        return False
    return True

def validate_student_input(student_code, full_name, class_name, email, phone, cccd, address):
    if student_code.strip() == "":
        return False, "Mã sinh viên không được để trống."

    if full_name.strip() == "":
        return False, "Họ tên không được để trống."

    if class_name.strip() == "":
        return False, "Lớp không được để trống. "

    if not is_valid_email(email):
        return False, "Email không đúng định dạng."

    if not is_valid_phone(phone.strip()):
        return False, "Số điện thoại không đúng định dạng."

    if not is_valid_cccd(cccd.strip()):
        return False, "CCCD không đúng định dạng."

    if address.strip() == "":
        return False, "Địa chỉ không được để trống."

    return True, "Hợp lệ."