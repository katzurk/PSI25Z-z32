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
    
    def generate_keys(self):
            private_key = random.randint(1, P-2)
            public_key = pow(G, private_key, P)
            return private_key, public_key
    
    def set_session_key(self, server_key, private_key):
        self.session_key = pow(server_key, private_key, P)
        self.msg_count = 0
        self.connected = True

    
    def connect(self):
        if self.connected:
            print("[!] Already connected.")
            return

        print(f"[*] Connecting to {HOST}:{PORT}...")
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))

            # Generate DH keys
            private_key, public_key = self.generate_keys()

            # 1. Send ClientHello
            client_hello = struct.pack(CLIENT_HELLO_FMT, MSG_CLIENT_HELLO, P, G, public_key)
            self.sock.sendall(client_hello)
            print("Sent ClientHello.")

            # 2. Receive ServerHello
            data = recv_nbytes(self.sock, struct.calcsize(SERVER_HELLO_FMT))
            header, server_key = struct.unpack(SERVER_HELLO_FMT, data)
            
            if header != MSG_SERVER_HELLO:
                raise ValueError("[!] Invalid ServerHello header")

            # Compute shared secret
            self.set_session_key(server_key, private_key)
            print(f"Connected. Session key established: {self.session_key}")

        except ConnectionRefusedError:
            print("[!] Connection refused.")
        except Exception as e:
            print(f'[!] {e}')
            self.cleanup()

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
    session = ClientSession()

    try:
        session.connect()
        while True:
            try:
                user_input = input("Client > ")

                plaintext = user_input.encode()
                ciphertext = otp_xor(plaintext, session.session_key, session.msg_count)
                packet = encode_message(MSG_REGULAR, ciphertext, session.session_key)
                session.sock.sendall(packet)
                print(f"> Sent message (No. {session.msg_count})")
                session.msg_count += 1

            except KeyboardInterrupt:
                end_msg = b"EndSession"
                ciphertext = otp_xor(end_msg, session.session_key, session.msg_count)
                packet = encode_message(MSG_END_SESSION, ciphertext, session.session_key)
                session.sock.sendall(packet)
                print("\n> Client shutting down...")
                break

    except ConnectionRefusedError:
        print("Error: Could not connect to server.")
    except Exception as e:
        print(f'Error: {e}')


if __name__ == "__main__":
    main()
