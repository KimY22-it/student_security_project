from connect_db import get_connection
from masking import mask_email, mask_phone, mask_cccd, mask_address
from encryption import encrypt, decrypt


def is_student_code_exists(student_code):
    conn = get_connection()
    if conn is None:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return False
    cursor = conn.cursor()
    sql = "SELECT id FROM students WHERE student_code = %s"
    cursor.execute(sql, (student_code,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def is_digits(s):
    for ch in s:
        if ch < '0' or ch > '9':
            return False
    return True

def is_valid_email(email):
    if '@' not in email:
        return False
    part = email.split('@')
    if len(part) != 2:
        return False
    name_part, domain_part = part
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
    email = input("Nhập email: ")
    while(len(email.strip()) == 0):
        print("Email không được để trống. Vui lòng nhập lại.")
        email = input("Nhập email: ")
    while(not is_valid_email(email)):
        print("Email không hợp lệ. Vui lòng nhập lại.")
        email = input("Nhập email: ")
    return email

def input_phone():
    phone = input("Nhập số điện thoại: ")
    while(len(phone.strip()) == 0):
        print("Số điện thoại không được để trống. Vui lòng nhập lại.")
        phone = input("Nhập số điện thoại: ")
    while(not is_valid_phone(phone)):
        print("Số điện thoại không hợp lệ. Vui lòng nhập lại.")
        phone = input("Nhập số điện thoại: ")
    return phone

def input_cccd():
    cccd = input("Nhập số CCCD: ")
    while(len(cccd.strip()) == 0):
        print("Số CCCD không được để trống. Vui lòng nhập lại.")
        cccd = input("Nhập số CCCD: ")
    while(not is_valid_cccd(cccd)):
        print("Số CCCD không hợp lệ. Vui lòng nhập lại.")
        cccd = input("Nhập số CCCD: ")
    return cccd

def input_address():
    address = input("Nhập địa chỉ: ")
    while(len(address.strip()) == 0):
        print("Địa chỉ không được để trống. Vui lòng nhập lại.")
        address = input("Nhập địa chỉ: ")
    return address

def input_student_code():
    student_code = input("Nhập mã sinh viên: ")
    while(len(student_code.strip()) == 0):
        print("Mã sinh viên không được để trống. Vui lòng nhập lại.")
        student_code = input("Nhập mã sinh viên: ")
    while(is_student_code_exists(student_code)):
        print("Mã sinh viên đã tồn tại. Vui lòng nhập lại.")
        student_code = input("Nhập mã sinh viên: ")
    return student_code

def input_full_name():
    full_name = input("Nhập tên sinh viên: ")
    while(len(full_name.strip()) == 0):
        print("Tên sinh viên không được để trống. Vui lòng nhập lại.")
        full_name = input("Nhập tên sinh viên: ")
    return full_name

def input_class_name():
    class_name = input("Nhập lớp: ")
    while(len(class_name.strip()) == 0):
        print("Lớp không được để trống. Vui lòng nhập lại.")
        class_name = input("Nhập lớp: ")
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
    sql = "INSERT INTO students (student_code, full_name, class_name, email, phone, cccd, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    value = (student_code, full_name, class_name, encrypt(email), encrypt(phone), encrypt(cccd), encrypt(address))
    
    try:
        cursor.execute(sql, value)
        conn.commit()
        print("Thêm sinh viên thành công.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()    

def display_student(student):
    print("\n")
    print('*' * 20)
    print(f"Mã sinh viên: {student['student_code']}\n")
    print(f"Họ tên: {student['full_name']}\n")
    print(f"Lớp: {student['class_name']}\n")
    print(f"Email: {student['email']}\n")
    print(f"Số điện thoại: {student['phone']}\n")
    print(f"Số CCCD: {student['cccd']}\n")
    print(f"Địa chỉ: {student['address']}\n")
    print(f"Ngày tạo: {student['create_at']}\n")
    print("\n")

def view_students(role):
    conn = get_connection()
    if conn is None:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return
    cursor = conn.cursor()
    sql = "SELECT student_code, full_name, class_name, email, phone, cccd, address, create_at FROM students"
    cursor.execute(sql)
    students = cursor.fetchall()
    if len(students) == 0:
        print("Không có sinh viên nào.")
        return
    for student in students:
        student_data = {
            'student_code': student[0],
            'full_name': student[1],
            'class_name': student[2],
            'email': mask_email(decrypt(student[3])) if role == 'user' else decrypt(student[3]),
            'phone': mask_phone(decrypt(student[4])) if role == 'user' else decrypt(student[4]),
            'cccd': mask_cccd(decrypt(student[5])) if role == 'user' else decrypt(student[5]),
            'address': mask_address(decrypt(student[6])) if role == 'user' else decrypt(student[6]),
            'create_at': student[7]
        }
        display_student(student_data)
    cursor.close()
    conn.close()
    
def delete_student(): 
    student_code = input("Nhập mã sinh viên cần xóa: ")
    conn = get_connection()
    if conn is None:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return
    if not is_student_code_exists(student_code):
        print("Mã sinh viên không tồn tại.")
        return
    cursor = conn.cursor()
    sql = "DELETE FROM students WHERE student_code = %s"
    try:
        cursor.execute(sql, (student_code,))
        conn.commit()
        if cursor.rowcount > 0:
            print("Xóa sinh viên thành công.")
        else:
            print("Không tìm thấy sinh viên với mã đã nhập.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


