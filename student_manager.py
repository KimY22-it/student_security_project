from connect_db import get_connection
from masking import mask_email, mask_phone, mask_cccd, mask_address
from encryption import encrypt, decrypt


def is_student_code_exists(student_code):
    conn = get_connection()
    if conn is None:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return False

    cursor = conn.cursor()
    try:
        sql = "SELECT id FROM students WHERE student_code = %s"
        cursor.execute(sql, (student_code,))
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        conn.close()


def is_digits(s):
    for ch in s:
        if ch < '0' or ch > '9':
            return False
    return True


def is_valid_email(email):
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


def input_email():
    email = input("Nhập email: ").strip()
    while len(email) == 0:
        print("Email không được để trống. Vui lòng nhập lại.")
        email = input("Nhập email: ").strip()
    while(not is_valid_email(email)):
        print("Email không hợp lệ. Vui lòng nhập lại.")
        email = input("Nhập email: ").strip()

    return email


def input_phone():
    phone = input("Nhập số điện thoại: ").strip()
    while(len(phone) == 0):
        print("Số điện thoại không được để trống. Vui lòng nhập lại.")
        phone = input("Nhập số điện thoại: ").strip()
    while(not is_valid_phone(phone)):
        print("Số điện thoại không hợp lệ. Vui lòng nhập lại.")
        phone = input("Nhập số điện thoại: ").strip()

    return phone


def input_cccd():
    cccd = input("Nhập số CCCD: ").strip()
    while(len(cccd) == 0):
        print("Số CCCD không được để trống. Vui lòng nhập lại.")
        cccd = input("Nhập số CCCD: ").strip()
    while(not is_valid_cccd(cccd)):
        print("Số CCCD không hợp lệ. Vui lòng nhập lại.")
        cccd = input("Nhập số CCCD: ").strip()

    return cccd


def input_address():
    address = input("Nhập địa chỉ: ").strip()
    while(len(address) == 0):
        print("Địa chỉ không được để trống. Vui lòng nhập lại.")
        address = input("Nhập địa chỉ: ").strip()
        address = input("Nhập địa chỉ: ").strip()
    return address


def input_student_code():
    student_code = input("Nhập mã sinh viên: ").strip()
    while(len(student_code) == 0):
        print("Mã sinh viên không được để trống. Vui lòng nhập lại.")
        student_code = input("Nhập mã sinh viên: ").strip()
    while(is_student_code_exists(student_code)):
        print("Mã sinh viên đã tồn tại. Vui lòng nhập lại.")
        student_code = input("Nhập mã sinh viên: ").strip()
    return student_code


def input_full_name():
    full_name = input("Nhập tên sinh viên: ").strip()
    while(len(full_name) == 0):
        print("Tên sinh viên không được để trống. Vui lòng nhập lại.")
        full_name = input("Nhập tên sinh viên: ").strip()
    return full_name


def input_class_name():
    class_name = input("Nhập lớp: ")
    while(len(class_name.strip()) == 0):
        print("Lớp không được để trống. Vui lòng nhập lại.")
        class_name = input("Nhập lớp: ").strip()
    return class_name


def add_student():
    print("Thêm sinh viên")

    student_code = input_student_code()
    full_name = input_full_name()
    class_name = input_class_name()
    email = input_email()
    phone = input_phone()
    cccd = input_cccd()
    address = input_address()

    conn = get_connection()
    if conn is None:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return

    cursor = conn.cursor()
    sql = """
        INSERT INTO students
        (student_code, full_name, class_name, email, phone, cccd, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        student_code,
        full_name,
        class_name,
        encrypt(email),
        encrypt(phone),
        encrypt(cccd),
        encrypt(address)
    )

    try:
        cursor.execute(sql, values)
        conn.commit()
        print("Thêm sinh viên thành công.")
    except Exception as e:
        print(f"Lỗi khi thêm sinh viên: {e}")
    finally:
        cursor.close()
        conn.close()


def _build_student_full(row):
    return {
        "student_code": row[0],
        "full_name": row[1],
        "class_name": row[2],
        "email": decrypt(row[3]),
        "phone": decrypt(row[4]),
        "cccd": decrypt(row[5]),
        "address": decrypt(row[6]),
        "create_at": row[7]
    }


def _build_student_masked(row):
    full_student = _build_student_full(row)

    return {
        "student_code": full_student["student_code"],
        "full_name": full_student["full_name"],
        "class_name": full_student["class_name"],
        "email": mask_email(full_student["email"]),
        "phone": mask_phone(full_student["phone"]),
        "cccd": mask_cccd(full_student["cccd"]),
        "address": mask_address(full_student["address"]),
        "create_at": full_student["create_at"]
    }


def get_students_full():
    """
    Dùng cho admin / xử lý nội bộ:
    đọc DB -> giải mã -> trả dữ liệu đầy đủ
    """
    conn = get_connection()
    if conn is None:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return []

    cursor = conn.cursor()
    sql = """
        SELECT student_code, full_name, class_name, email, phone, cccd, address, create_at
        FROM students
        ORDER BY id DESC
    """

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [_build_student_full(row) for row in rows]
    except Exception as e:
        print(f"Lỗi khi lấy danh sách sinh viên: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def get_students_masked():
    """
    Dùng cho API / user thường:
    đọc DB -> giải mã -> masking -> trả dữ liệu đã che
    """
    conn = get_connection()
    if conn is None:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return []

    cursor = conn.cursor()
    sql = """
        SELECT student_code, full_name, class_name, email, phone, cccd, address, create_at
        FROM students
        ORDER BY id DESC
    """

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [_build_student_masked(row) for row in rows]
    except Exception as e:
        print(f"Lỗi khi lấy danh sách sinh viên: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def display_student(student):
    print("\n" + "*" * 20)
    print(f"Mã sinh viên: {student['student_code']}")
    print(f"Họ tên: {student['full_name']}")
    print(f"Lớp: {student['class_name']}")
    print(f"Email: {student['email']}")
    print(f"Số điện thoại: {student['phone']}")
    print(f"Số CCCD: {student['cccd']}")
    print(f"Địa chỉ: {student['address']}")
    print(f"Ngày tạo: {student['create_at']}")
    print("*" * 20 + "\n")


def view_students(role):
    """
    Giữ tương thích với main.py hiện tại:
    - admin -> xem full data
    - user  -> xem masked data
    """
    if role == "admin":
        students = get_students_full()
    else:
        students = get_students_masked()

    if len(students) == 0:
        print("Không có sinh viên nào.")
        cursor.close()
        conn.close()
        return

    for student in students:
        display_student(student)


def delete_student():
    student_code = input("Nhập mã sinh viên cần xóa: ").strip()

    conn = get_connection()
    if conn is None:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return

    try:
        if not is_student_code_exists(student_code):
            print("Mã sinh viên không tồn tại.")
            return

        cursor = conn.cursor()
        try:
            sql = "DELETE FROM students WHERE student_code = %s"
            cursor.execute(sql, (student_code,))
            conn.commit()

            if cursor.rowcount > 0:
                print("Xóa sinh viên thành công.")
            else:
                print("Không tìm thấy sinh viên với mã đã nhập.")
        finally:
            cursor.close()
    except Exception as e:
        print(f"Lỗi khi xóa sinh viên: {e}")
    finally:
        conn.close()