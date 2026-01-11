import socket
import struct
import random
import hashlib
import hmac
import time
from protocol.protocol import (
    otp_xor, encode_message, decode_message, recv_nbytes,
    MSG_CLIENT_HELLO, MSG_SERVER_HELLO, MSG_ENCRYPTED, MSG_END_SESSION,
    CLIENT_HELLO_FMT, SERVER_HELLO_FMT, ENCRYPTED_FMT
)

HOST = "z32-server-projekt"
PORT = 5000


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
        data = recv_nbytes(sock, struct.calcsize("!BI"))
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