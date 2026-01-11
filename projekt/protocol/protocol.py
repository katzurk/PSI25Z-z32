import random
import struct
import hashlib
import hmac

MSG_CLIENT_HELLO = 0x01
MSG_SERVER_HELLO = 0x02
MSG_ENCRYPTED = 0x04
MSG_END_SESSION = 0x02
MSG_REGULAR = 0x01

CLIENT_HELLO_FMT = "!BIII"
SERVER_HELLO_FMT = "!BI"
ENCRYPTED_FMT = "!BI"
MAC_SIZE = 32


def otp_xor(data, key, msg_count):
    seed = key + msg_count
    rng = random.Random(seed)
    key_stream = bytes([rng.randint(0, 255) for i in range(len(data))])
    return bytes([b ^ k for b, k in zip(data, key_stream)])


def encode_message(msg_type, ciphertext, key):
    length = 1 + len(ciphertext)
    header = struct.pack(ENCRYPTED_FMT, MSG_ENCRYPTED, length)
    payload = struct.pack("!B", msg_type) + ciphertext

    mac = hmac.new(key.to_bytes(4, 'big'), header + payload, hashlib.sha256).digest()

    return header + payload + mac


def decode_message(sock, key):
    header = recv_nbytes(sock, 5)
    if header[0] != 0x04:
        raise ValueError("Incorrect message type")
    length = struct.unpack("!I", header[1:])[0]

    payload_mac = recv_nbytes(sock, length + 32)
    payload = payload_mac[:length]

    recv_mac = payload_mac[length:]
    calc_mac = hmac.new(key.to_bytes(4, 'big'), header + payload, hashlib.sha256).digest()
    if not hmac.compare_digest(calc_mac, recv_mac):
        raise ValueError("Incorrect MAC")

    msg_type = payload[0]
    ciphertext = payload[1:]

    return msg_type, ciphertext


def recv_nbytes(sock, n):
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk
    return data
