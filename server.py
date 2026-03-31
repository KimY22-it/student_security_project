import socket
import json
from auth import check_login
from student_manager import (
    get_students_for_display,
    add_student_data,
    delete_student_by_code
)

HOST = "127.0.0.1"
PORT = 5000


def handle_request(payload):
    action = payload.get("action")

    if action == "login":
        username = payload.get("username", "")
        password = payload.get("password", "")
        user = check_login(username, password)

        if user is None:
            return {"success": False, "message": "Sai tài khoản hoặc mật khẩu."}

        return {"success": True, "user": user}

    elif action == "get_students":
        role = payload.get("role", "user")
        students = get_students_for_display(role)
        return {"success": True, "students": students}

    elif action == "add_student":
        data = payload.get("data", {})

        success, message = add_student_data(
            data.get("student_code", ""),
            data.get("full_name", ""),
            data.get("class_name", ""),
            data.get("email", ""),
            data.get("phone", ""),
            data.get("cccd", ""),
            data.get("address", "")
        )

        return {"success": success, "message": message}

    elif action == "delete_student":
        code = payload.get("student_code", "")
        success, message = delete_student_by_code(code)
        return {"success": success, "message": message}

    return {"success": False, "message": "Yêu cầu không hợp lệ."}


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"Server đang chạy tại {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print("Đã kết nối từ:", addr)

        data = conn.recv(65536).decode("utf-8")
        if not data:
            conn.close()
            continue

        payload = json.loads(data)
        response = handle_request(payload)

        conn.sendall(json.dumps(response, ensure_ascii=False).encode("utf-8"))
        conn.close()


if __name__ == "__main__":
    start_server()