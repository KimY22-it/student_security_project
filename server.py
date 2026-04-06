import socket
import json
import secrets
import time
from auth import check_login, register_user
from personal_info_manager import get_personal_info, get_all_personal_info
from dh import dh_handshake_server, send_frame, recv_frame, channel_encrypt, channel_decrypt

HOST = "127.0.0.1"
PORT = 5000

CLIENT_TIMEOUT = 10
SERVER_ACCEPT_TIMEOUT = 2
SESSION_TIMEOUT = 10 * 60 
ACTIVE_SESSIONS = {}

def _create_session(user: dict) -> str:
    session_token = secrets.token_hex(32)
    now = time.time()

    ACTIVE_SESSIONS[session_token] = {
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "data_key": user.get("data_key"),
        "created_at": now,
        "last_seen": now,
    }
    return session_token


def _get_session(payload: dict):
    session_token = payload.get("session_token", "")
    if not session_token:
        return None

    session = ACTIVE_SESSIONS.get(session_token)
    if session is None:
        return None

    now = time.time()

    # Hết hạn nếu không hoạt động quá lâu
    if now - session["last_seen"] > SESSION_TIMEOUT:
        del ACTIVE_SESSIONS[session_token]
        return None

    # Cập nhật lần hoạt động cuối
    session["last_seen"] = now
    return session

def cleanup_expired_sessions():
    now = time.time()
    expired_tokens = []

    for token, session in ACTIVE_SESSIONS.items():
        if now - session["last_seen"] > SESSION_TIMEOUT:
            expired_tokens.append(token)

    for token in expired_tokens:
        del ACTIVE_SESSIONS[token]

def handle_request(payload: dict) -> dict:
    """Xử lý payload (đã giải mã), trả về response dict."""
    action = payload.get("action")

    if action == "login":
        username = payload.get("username", "")
        password = payload.get("password", "")
        user = check_login(username, password)

        if user is None:
            return {"success": False, "message": "Sai tài khoản hoặc mật khẩu."}

        session_token = _create_session(user)
        return {
            "success": True,
            "user": {
                "username": user["username"],
                "role": user["role"],
            },
            "session_token": session_token,
        }


    elif action == "register":
        data = payload.get("data", {})
        success, message = register_user(
            username=data.get("username", ""),
            password=data.get("password", ""),
            fullname=data.get("fullname", ""),
            gender=data.get("gender", ""),
            email=data.get("email", ""),
            cccd=data.get("cccd", ""),
            phone=data.get("phone", ""),
        )
        return {"success": success, "message": message}

    elif action == "get_my_info":
        session = _get_session(payload)
        
        if session is None:
            return {"success": False, "message": "Phiên đăng nhập không hợp lệ hoặc đã hết hạn."}
        if session["role"] != "user":
            return {"success": False, "message": "Chỉ user thường mới được xem thông tin cá nhân."}

        if not session.get("data_key"):
            return {"success": False, "message": "Không tìm thấy khóa dữ liệu của phiên hiện tại."}
        
        info = get_personal_info(session["id"], session["data_key"])
        if info:
            return {"success": True, "info": info}
        return {"success": False, "message": "Không tìm thấy thông tin hoặc giải mã thất bại."}
        
    elif action == "get_all_info":
        session = _get_session(payload)
        if session is None:
            return {"success": False, "message": "Phiên đăng nhập không hợp lệ hoặc đã hết hạn."}
        if session["role"] != "admin":
            return {"success": False, "message": "Chỉ admin mới được xem thông tin cá nhân."}
        info_list = get_all_personal_info()
        return {"success": True, "info_list": info_list}
    elif action == "logout":
        session_token = payload.get("session_token", "")
        if session_token in ACTIVE_SESSIONS:
            del ACTIVE_SESSIONS[session_token]
            return {"success": True, "message": "Đăng xuất thành công."}
        return {"success": False, "message": "Phiên đăng nhập không hợp lệ hoặc đã hết hạn."}

    return {"success": False, "message": "Yêu cầu không hợp lệ."}


def handle_connection(conn, addr):
    """Xử lý 1 kết nối: DH handshake → nhận request mã hóa → gửi response mã hóa."""
    print(f"Kết nối từ: {addr}")
    conn.settimeout(CLIENT_TIMEOUT)
    try:
        # 1. DH Handshake – thiết lập session_key
        session_key = dh_handshake_server(conn)

        # 2. Nhận payload đã mã hóa
        encrypted_payload = recv_frame(conn)

        # 3. Giải mã
        plaintext = channel_decrypt(session_key, encrypted_payload)
        payload   = json.loads(plaintext.decode("utf-8"))

        # 4. Xử lý logic
        response = handle_request(payload)

        # 5. Mã hóa response và gửi về
        response_bytes     = json.dumps(response, ensure_ascii=False).encode("utf-8")
        encrypted_response = channel_encrypt(session_key, response_bytes)
        send_frame(conn, encrypted_response)

    except socket.timeout:
        print(f"  [Lỗi] {addr}: Client phản hồi chậm bị timeout.")
    except Exception as e:
        print(f"  [Lỗi] {addr}: {e}")
    finally:
        conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    server.settimeout(SERVER_ACCEPT_TIMEOUT)
    print(f"Server đang chạy tại {HOST}:{PORT} (DH-encrypted)")

    while True:
        try:
            cleanup_expired_sessions()
            conn, addr = server.accept()
            handle_connection(conn, addr)
        except socket.timeout:
            cleanup_expired_sessions()
            continue
        except KeyboardInterrupt:
            print("Dừng server.")
            break
        except Exception as e:
            print(f"Lỗi accept: {e}")
    server.close()


if __name__ == "__main__":
    start_server()