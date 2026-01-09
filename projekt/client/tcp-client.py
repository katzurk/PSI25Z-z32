import socket
import struct
import random
import hashlib
import hmac
import time

HOST = "z32-server-projekt"
PORT = 5000

MSG_CLIENT_HELLO = 0x01
MSG_SERVER_HELLO = 0x02
MSG_ENCRYPTED = 0x04
MSG_END_SESSION = 0x02

CLIENT_HELLO_FMT = "!BIII"
ENCRYPTED_FMT = "!BI"
MAC_SIZE = 32

def otp_xor(data, key, msg_count):
    seed = key + msg_count
    rng = random.Random(seed)
    key_stream = bytes([rng.randint(0, 255) for i in range(len(data))])
    return bytes([b ^ k for b, k in zip(data, key_stream)])

def encode_message(msg_type, message, key, msg_count):
    ciphertext = otp_xor(message, key, msg_count)
    length = 1 + len(ciphertext)
    header = struct.pack(ENCRYPTED_FMT, MSG_ENCRYPTED, length)
    payload = struct.pack("!B", msg_type) + ciphertext
    mac = hmac.new(key.to_bytes(4, 'big'), header + payload, hashlib.sha256).digest()
    return header + payload + mac

def recv_n(sock, n):
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk
    return data

def main():
    p = 14
    g = 5
    a = random.randint(1, p-2)
    A = pow(g, a, p)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        # ClientHello
        client_hello = struct.pack(CLIENT_HELLO_FMT, MSG_CLIENT_HELLO, p, g, A)
        sock.sendall(client_hello)
        print("Sent ClientHello")

        # ServerHello
        data = recv_n(sock, struct.calcsize("!BI"))
        header, B = struct.unpack("!BI", data)
        if header != MSG_SERVER_HELLO:
            raise ValueError("Incorrect message type")
        print(f"Received ServerHello: B={B}")

        session_key = pow(B, a, p)

        time.sleep(30)

        # EndSession
        msg_count = 0
        end_msg = b"EndSession"
        packet = encode_message(MSG_END_SESSION, end_msg, session_key, msg_count)
        sock.sendall(packet)
        print("Sent EndSession")

if __name__ == "__main__":
    main()