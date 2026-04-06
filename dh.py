#!/usr/bin/env python3
"""
Diffie-Hellman Key Exchange – RFC 3526 Group 14 (2048-bit)

Giao thức:
  1. Server sinh (server_priv, server_pub), gửi (p, g, server_pub) cho client.
  2. Client sinh (client_priv, client_pub), gửi client_pub cho server.
  3. Cả hai tính shared_secret = SHA-256(pow(other_pub, my_priv, p))[:16]
     => session_key dùng để mã hóa AES kênh truyền.
"""

from encryption import aes_encrypt_bytes
import os
import hashlib
import struct

# ---------------------------------------------------------------------------
# RFC 3526 Group 14 – Safe Prime 2048-bit
# p = 2^2048 − 2^1984 + 2^64 * ⌊2^1918 * π⌋ + 124
# g = 2
# ---------------------------------------------------------------------------
DH_P = int(
    "FFFFFFFFFFFFFFFF" "C90FDAA22168C234" "C4C6628B80DC1CD1"
    "29024E088A67CC74" "020BBEA63B139B22" "514A08798E3404DD"
    "EF9519B3CD3A431B" "302B0A6DF25F1437" "4FE1356D6D51C245"
    "E485B576625E7EC6" "F44C42E9A637ED6B" "0BFF5CB6F406B7ED"
    "EE386BFB5A899FA5" "AE9F24117C4B1FE6" "49286651ECE45B3D"
    "C2007CB8A163BF05" "98DA48361C55D39A" "69163FA8FD24CF5F"
    "83655D23DCA3AD96" "1C62F356208552BB" "9ED529077096966D"
    "670C354E4ABC9804" "F1746C08CA18217C" "32905E462E36CE3B"
    "E39E772C180E8603" "9B2783A2EC07A28F" "B5C55DF06F4C52C9"
    "DE2BCBF695581718" "3995497CEA956AE5" "15D2261898FA0510"
    "15728E5A8AACAA68" "FFFFFFFFFFFFFFFF",
    16,
)
DH_G = 2


# ---------------------------------------------------------------------------
# DH Key Generation & Shared Secret
# ---------------------------------------------------------------------------

def generate_dh_private_key() -> int:
    """Sinh private key ngẫu nhiên (256 bytes, nằm trong [2, p-2])."""
    raw = int.from_bytes(os.urandom(256), "big")
    return raw % (DH_P - 2) + 2


def generate_dh_public_key(private_key: int) -> int:
    """Tính public key = g^priv mod p  (modular exponentiation nhanh)."""
    return pow(DH_G, private_key, DH_P)


def compute_session_key(their_public: int, my_private: int) -> bytes:
    """
    Tính shared_secret = their_pub^my_priv mod p
    Băm SHA-256, lấy 16 bytes đầu làm AES-128 session key.
    """
    shared_int = pow(their_public, my_private, DH_P)
    shared_bytes = shared_int.to_bytes(256, "big")
    return hashlib.sha256(shared_bytes).digest()[:16]


# ---------------------------------------------------------------------------
# Channel Framing – độ dài 4 bytes big-endian + data
# ---------------------------------------------------------------------------

def send_frame(conn, data: bytes) -> None:
    """Gửi frame: [4-byte length][data]"""
    conn.sendall(struct.pack(">I", len(data)) + data)


def recv_frame(conn) -> bytes:
    """Nhận frame: đọc 4-byte length trước, sau đó đọc đủ data."""
    header = _recv_exactly(conn, 4)
    length = struct.unpack(">I", header)[0]
    return _recv_exactly(conn, length)


def _recv_exactly(conn, n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Kết nối bị đóng đột ngột.")
        buf += chunk
    return buf


# ---------------------------------------------------------------------------
# Channel Encryption – AES-CBC dùng session_key (không qua PBKDF2)
# ---------------------------------------------------------------------------

def channel_encrypt(session_key: bytes, plaintext: bytes) -> bytes:
    from encryption import aes_encrypt_bytes
    ciphertext = aes_encrypt_bytes(session_key, plaintext)
    return ciphertext


def channel_decrypt(session_key: bytes, data: bytes) -> bytes:
    from encryption import aes_decrypt_bytes
    plaintext = aes_decrypt_bytes(session_key, data)
    return plaintext

# ---------------------------------------------------------------------------
# DH Handshake Helpers
# ---------------------------------------------------------------------------

import json


def dh_handshake_server(conn) -> bytes:
    """
    Thực hiện DH handshake phía SERVER.
    Trả về session_key (16 bytes).
    """
    server_priv = generate_dh_private_key()
    server_pub  = generate_dh_public_key(server_priv)

    # Gửi params cho client (plain – DH public values không cần bí mật)
    params = json.dumps({
        "p":          str(DH_P),
        "g":          str(DH_G),
        "server_pub": str(server_pub),
    }).encode("utf-8")
    send_frame(conn, params)

    # Nhận public key của client
    client_msg = json.loads(recv_frame(conn).decode("utf-8"))
    client_pub = int(client_msg["client_pub"])

    session_key = compute_session_key(client_pub, server_priv)
    print(f"  [DH OK] ")
    return session_key


def dh_handshake_client(conn) -> bytes:
    """
    Thực hiện DH handshake phía CLIENT.
    Trả về session_key (16 bytes).
    """
    # Nhận params từ server
    server_msg = json.loads(recv_frame(conn).decode("utf-8"))
    p          = int(server_msg["p"])
    g          = int(server_msg["g"])
    server_pub = int(server_msg["server_pub"])

    client_priv = generate_dh_private_key()
    client_pub  = pow(g, client_priv, p)

    # Gửi public key cho server
    send_frame(conn, json.dumps({"client_pub": str(client_pub)}).encode("utf-8"))

    session_key = compute_session_key(server_pub, client_priv)
    return session_key
