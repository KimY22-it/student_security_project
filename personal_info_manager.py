from db.connect_db import get_connection
from encryption import decrypt

def get_personal_info(account_id, data_key: bytes):
    """
    Lấy thông tin cá nhân của user và giải mã bằng data_key.
    data_key được truyền vào từ session sau khi đăng nhập thành công.
    """
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor(dictionary=False)
    sql = """
        SELECT fullname, gender, email_encrypt, phone_encrypt, cccd_encrypt
        FROM personal_information
        WHERE account_id = %s
    """
    cursor.execute(sql, (account_id,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return None

    email = decrypt(row[2], data_key) if row[2] else ""
    phone = decrypt(row[3], data_key) if row[3] else ""
    cccd  = decrypt(row[4], data_key) if row[4] else ""

    return {
        "fullname": row[0],
        "gender":   row[1],
        "email":    email,
        "phone":    phone,
        "cccd":     cccd
    }

def get_all_personal_info():
    """
    Dành cho Admin: Lấy danh sách toàn bộ thông tin. Admin chỉ thấy bản mã.
    """
    conn = get_connection()
    if conn is None:
        return []

    cursor = conn.cursor(dictionary=False)
    # Lấy thêm thông tin username để dễ nhận biết
    sql = """
        SELECT a.username, p.fullname, p.gender, p.email_encrypt, p.phone_encrypt, p.cccd_encrypt
        FROM personal_information p
        JOIN accounts a ON p.account_id = a.id
        ORDER BY a.id ASC
    """
    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    users_info = []
    for row in rows:
        users_info.append({
            "username": row[0],
            "fullname": row[1],
            "gender": row[2],
            "email": row[3], # Bản mã
            "phone": row[4], # Bản mã
            "cccd": row[5]   # Bản mã
        })
    return users_info
