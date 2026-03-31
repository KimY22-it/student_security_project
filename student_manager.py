from connect_db import get_connection
from masking import mask_email, mask_phone, mask_cccd
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





def get_students_for_display(role):
    conn = get_connection()
    if conn is None:
        return []

    cursor = conn.cursor()
    sql = """
        SELECT student_code, full_name, class_name, email, phone, cccd, address
        FROM students
        ORDER BY id ASC
    """
    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    students = []

    for row in rows:
        try:
            email = decrypt(row[3])
            phone = decrypt(row[4])
            cccd = decrypt(row[5])
        except Exception as e:
            print(f"Lỗi khi giải mã dữ liệu sinh viên: {e}")
            continue

        if role == "user":
            email = mask_email(email)
            phone = mask_phone(phone)
            cccd = mask_cccd(cccd)

        student = {
            "student_code": row[0],
            "full_name": row[1],
            "class_name": row[2],
            "email": email,
            "phone": phone,
            "cccd": cccd,
            "address": row[6]
        }
        students.append(student)

    return students

def add_student_data(student_code, full_name, class_name, email, phone, cccd, address):
    student_code = student_code.strip()
    full_name = full_name.strip()
    class_name = class_name.strip()
    email = email
    phone = phone
    cccd = cccd
    address = address.strip()

    if is_student_code_exists(student_code):
        return False, "Mã sinh viên đã tồn tại."

    conn = get_connection()
    if conn is None:
        return False, "Không thể kết nối đến cơ sở dữ liệu."

    cursor = conn.cursor()
    sql = """
        INSERT INTO students (student_code, full_name, class_name, email, phone, cccd, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        student_code,
        full_name,
        class_name,
        email,
        phone,
        cccd,
        address
    )

    try:
        cursor.execute(sql, values)
        conn.commit()
        return True, "Thêm sinh viên thành công."
    except Exception as e:
        return False, f"Lỗi: {e}"
    finally:
        cursor.close()
        conn.close()


def delete_student_by_code(student_code):
    student_code = student_code.strip()

    if student_code == "":
        return False, "Vui lòng nhập mã sinh viên."

    conn = get_connection()
    if conn is None:
        return False, "Không thể kết nối đến cơ sở dữ liệu."

    cursor = conn.cursor()

    sql_check = "SELECT id FROM students WHERE student_code = %s"
    cursor.execute(sql_check, (student_code,))
    result = cursor.fetchone()

    if result is None:
        cursor.close()
        conn.close()
        return False, "Mã sinh viên không tồn tại."

    sql_delete = "DELETE FROM students WHERE student_code = %s"
    try:
        cursor.execute(sql_delete, (student_code,))
        conn.commit()
        return True, "Xóa sinh viên thành công."
    except Exception as e:
        return False, f"Lỗi: {e}"
    finally:
        cursor.close()
        conn.close()