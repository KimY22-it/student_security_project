import socket
import json

from encryption import encrypt
from validation import  validate_student_input

HOST = "127.0.0.1"
PORT = 5000


def send_request(payload):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    client.sendall(data)

    response = client.recv(65536).decode("utf-8")
    client.close()

    return json.loads(response)


def login(username, password):
    return send_request({
        "action": "login",
        "username": username,
        "password": password
    })


def get_students(role):
    return send_request({
        "action": "get_students",
        "role": role
    })


def add_student(student_data):
    ok, message = validate_student_input(
        student_data.get("student_code", ""),
        student_data.get("full_name", ""),
        student_data.get("class_name", ""),
        student_data.get("email", ""),
        student_data.get("phone", ""),
        student_data.get("cccd", ""),
        student_data.get("address", "")
    )

    if not ok:
        return {"success": False, "message": message}

    encrypted_data = {
        "student_code": student_data.get("student_code", "").strip(),
        "full_name": student_data.get("full_name", "").strip(),
        "class_name": student_data.get("class_name", "").strip(),
        "email": encrypt(student_data.get("email", "").strip()),
        "phone": encrypt(student_data.get("phone", "").strip()),
        "cccd": encrypt(student_data.get("cccd", "").strip()),
        "address": student_data.get("address", "").strip()
    }

    return send_request({
        "action": "add_student",
        "data": encrypted_data
    })

def delete_student(student_code):
    return send_request({
        "action": "delete_student",
        "student_code": student_code
    })