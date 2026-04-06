import socket
import json
from dh import dh_handshake_client, send_frame, recv_frame, channel_encrypt, channel_decrypt

HOST = "127.0.0.1"
PORT = 5000

SOCKET_TIMEOUT = 10

_CURRENT_SESSION_TOKEN = None
_CURRENT_USER = None
_CURRENT_INFO = None
_CURRENT_INFO_LIST = None


def send_request(payload: dict) -> dict:
    """
    Gửi request tới server qua kênh mã hóa DH + AES.
    Mỗi lần gọi:
        1. Tạo socket mới (dùng địa chỉ ipv4 và )
        2. Kết nối tới server
        3. Thực hiện bắt tay DH để sinh session_key
        4. Dùng session_key đó để mã hóa dữ liệu
        5. Gửi lên server
        6. Nhận phản hồi từ server
        7. Giải mã phản hồi
        8. Trả dữ liệu về cho chương trình
    """
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.settimeout(SOCKET_TIMEOUT)
    
    try:
        conn.connect((HOST, PORT))
        # DH handshake
        session_key = dh_handshake_client(conn)

        # Mã hóa payload và gửi
        payload_bytes     = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        encrypted_payload = channel_encrypt(session_key, payload_bytes)
        send_frame(conn, encrypted_payload)

        # Nhận và giải mã response
        encrypted_response = recv_frame(conn)
        response_bytes     = channel_decrypt(session_key, encrypted_response)
        return json.loads(response_bytes.decode("utf-8"))
    except socket.timeout:
        return {"success": False, "message": "Kết nối tới server bị timeout."}
    except Exception as e:
        return {"success": False, "message": f"Lỗi hệ thống: {str(e)}"}
    finally:
        conn.close()


def login(username: str, password: str) -> dict:
    global _CURRENT_SESSION_TOKEN, _CURRENT_USER, _CURRENT_INFO, _CURRENT_INFO_LIST
    response = send_request({
        "action": "login",
        "username": username,
        "password": password,
    })

    if response.get("success"):
        _CURRENT_SESSION_TOKEN = response.get("session_token")
        _CURRENT_USER = response.get("user")
        _CURRENT_INFO = None
        _CURRENT_INFO_LIST = None

        role = (_CURRENT_USER or {}).get("role")
        if role == "user":
            info_response = get_my_info()
            if info_response.get("success"):
                _CURRENT_INFO = info_response.get("info")
                response["info"] = _CURRENT_INFO
        elif role == "admin":
            info_list_response = get_all_info()
            if info_list_response.get("success"):
                _CURRENT_INFO_LIST = info_list_response.get("info_list")
                response["info_list"] = _CURRENT_INFO_LIST
    else:
        _CURRENT_SESSION_TOKEN = None
        _CURRENT_USER = None
        _CURRENT_INFO = None
        _CURRENT_INFO_LIST = None

    return response




def register(data: dict) -> dict:
    return send_request({
        "action": "register",
        "data":   data,
    })


def get_my_info():
    if not _CURRENT_SESSION_TOKEN:
        return {"success": False, "message": "Bạn chưa đăng nhập."}
    return send_request({
        "action":       "get_my_info",
        "session_token": _CURRENT_SESSION_TOKEN,    
    })


def get_all_info():
    if not _CURRENT_SESSION_TOKEN:
        return {"success": False, "message": "Bạn chưa đăng nhập."}
    return send_request({
        "action": "get_all_info",
        "session_token": _CURRENT_SESSION_TOKEN,
    })

def logout() -> dict:
    global _CURRENT_SESSION_TOKEN, _CURRENT_USER, _CURRENT_INFO, _CURRENT_INFO_LIST

    if not _CURRENT_SESSION_TOKEN:
        return {"success": True, "message": "Bạn chưa đăng nhập."}

    response = send_request({
        "action": "logout",
        "session_token": _CURRENT_SESSION_TOKEN,
    })
    _CURRENT_SESSION_TOKEN = None
    _CURRENT_USER = None
    _CURRENT_INFO = None
    _CURRENT_INFO_LIST = None
    return response



def get_current_user():
    return _CURRENT_USER

def get_current_info():
    return _CURRENT_INFO

def get_current_info_list():
    return _CURRENT_INFO_LIST
