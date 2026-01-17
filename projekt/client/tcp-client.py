import socket
import struct
import random
import sys
from protocol.protocol import (
    otp_xor, encode_message, decode_message, recv_nbytes,
    MSG_CLIENT_HELLO, MSG_SERVER_HELLO, MSG_ENCRYPTED, MSG_END_SESSION,
    CLIENT_HELLO_FMT, SERVER_HELLO_FMT, ENCRYPTED_FMT, MSG_REGULAR
)

HOST = "z32-server-projekt"
PORT = 5000
P = 2147483647
G = 2

class ClientSession:
    def __init__(self):
        self.sock = None
        self.session_key = None
        self.msg_count = 0
        self.connected = False
    
    def connect(self):
        pass

    def send_message(self):
        pass

    def cleanup(self):
        if self.sock:
            self.sock.close()
        self.sock = None
        self.session_key = None
        self.msg_count = 0
        self.connected = False
        print("[*] Disconnected from server.")

def main():
    private_key = random.randint(1, P-2)
    public_key = pow(G, private_key, P)

    msg_count = 0

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))

            # ClientHello
            client_hello = struct.pack(CLIENT_HELLO_FMT, MSG_CLIENT_HELLO, P, G, public_key)
            sock.sendall(client_hello)
            print("Sent ClientHello.")

            # ServerHello
            data = recv_nbytes(sock, struct.calcsize(SERVER_HELLO_FMT))
            header, server_key = struct.unpack(SERVER_HELLO_FMT, data)
            if header != MSG_SERVER_HELLO:
                raise ValueError("Incorrect message type")

            session_key = pow(server_key, private_key, P)
            print("Established session key.")

            while True:
                try:
                    user_input = input("Client > ")

                    plaintext = user_input.encode()
                    ciphertext = otp_xor(plaintext, session_key, msg_count)
                    packet = encode_message(MSG_REGULAR, ciphertext, session_key)
                    sock.sendall(packet)
                    print(f"> Sent message (No. {msg_count})")
                    msg_count += 1

                except KeyboardInterrupt:
                    end_msg = b"EndSession"
                    ciphertext = otp_xor(end_msg, session_key, msg_count)
                    packet = encode_message(MSG_END_SESSION, ciphertext, session_key)
                    sock.sendall(packet)
                    print("\n> Client shutting down...")
                    break

    except ConnectionRefusedError:
        print("Error: Could not connect to server.")
    except Exception as e:
        print(f'Error: {e}')


if __name__ == "__main__":
    main()
