from connect_db import get_connection

def check_login(username, password):
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    sql = "SELECT id, username, password, role FROM accounts WHERE username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None:
        return None

    account_id = result[0]
    db_username = result[1]
    db_password = result[2]
    db_role = result[3]

    if password == db_password:
        return {
            "id": account_id,
            "username": db_username,
            "role": db_role
        }

    return None


def login():
    username = input("Nhập username: ").strip()
    password = input("Nhập password: ").strip()

    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    sql = "SELECT id, username, password, role FROM accounts WHERE username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None:
        print("Sai tài khoản.")
        return None

    account_id = result[0]
    db_username = result[1]
    db_password = result[2]
    db_role = result[3]

    if password == db_password:
        print("Đăng nhập thành công.")
        return {
            "id": account_id,
            "username": db_username,
            "role": db_role
        }

    print("Sai mật khẩu.")
    return None