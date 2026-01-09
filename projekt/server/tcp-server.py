import socket
import random
import sys
import struct
import threading
import time
from protocol import (
    otp_xor, encode_message, decode_message, recv_nbytes,
    MSG_CLIENT_HELLO, MSG_SERVER_HELLO, MSG_ENCRYPTED,
    CLIENT_HELLO_FMT, SERVER_HELLO_FMT, ENCRYPTED_FMT
)

HOST = "0.0.0.0"
PORT = 5000

connections = {}
connections_lock = threading.Lock()


def send_ServerHello(sock, public_key):
    msg = struct.pack(SERVER_HELLO_FMT, MSG_SERVER_HELLO, public_key)
    sock.sendall(msg)

def send_EndSession(sock, key, msg_count):
    msg = b"EndSession"
    ciphertext = otp_xor(msg, key, msg_count)
    packet = encode_message(0x02, msg, key)
    sock.sendall(packet)

def handle_client(client_sock, addr):
    host, port = addr

    with client_sock:
        try:
            # ClientHello
            data = recv_nbytes(client_sock, struct.calcsize(CLIENT_HELLO_FMT))
            header, p, g, client_key = struct.unpack(CLIENT_HELLO_FMT, data)
            if header != MSG_CLIENT_HELLO:
                raise ValueError("Incorrect message type")

            print(f"[{host}:{port}] ClientHello")

            # ServerHello
            private_key = random.randint(1, p-2)
            public_key = pow(g, private_key, p)
            send_ServerHello(client_sock, public_key)

            print(f"> Sent ServerHello to {host}:{port}")

            session_key = pow(client_key, private_key, p)

            with connections_lock:
                connections[(host, port)] = {
                    "socket": client_sock,
                    "key": session_key,
                    "msg_count": 0
                }

            while True:
                msg_type, ciphertext = decode_message(client_sock, session_key)
                with connections_lock:
                    msg_count = connections[(host, port)]["msg_count"]
                    connections[(host, port)]["msg_count"] += 1
                message = otp_xor(ciphertext, session_key, msg_count)

                if msg_type == 0x01:
                    print(f"[{host}:{port}] {message.decode()}")
                elif msg_type == 0x02:
                    print(f"[{host}:{port}] {message.decode()} (EndSession)")
                    break

        except Exception as e:
            print("Error:", e)

def close_connection(sock_id):
    with connections_lock:
        addr = list(connections.keys())[sock_id]
        client = connections.pop(addr)
        msg_count = client["msg_count"]
        key = client["key"]

        try:
            send_EndSession(client["socket"], key, msg_count)
            client["socket"].close()
        except Exception as e:
            print("Error:", e)

def close_all_connections():
    with connections_lock:
        addrs = list(connections.keys())

        for addr in addrs:
            try:
                with connections_lock:
                    client = connections.pop(addr, None)
                    if not client:
                        continue
                send_EndSession(client["socket"], client["key"], client["msg_count"])
                client["socket"].close()
            except Exception as e:
                print("Error:", e)


def handle_command(command):
    cmd = command.strip().split()

    # S - show connections
    if cmd[0] == "S":
        msg = "> Current connections:"
        if (len(connections) == 0):
            msg += "\nNo active connections"
        for idx, conn in enumerate(connections.items()):
            msg += f"\n{idx}. {conn[0]}"
        print(msg)

    # E <connection_idx> - end session
    elif cmd[0] == "E":
        pass
        # idx = int(cmd[1])
        # close_connection(idx)

    # C - close server
    elif cmd[0] == "C":
        pass
        # print("> Server shutting down...")
        # close_all_connections()
        # sys.exit(0)

def user_input_thread():
    while True:
        command = input()
        handle_command(command)


def main():
    n_client = 1

    if len(sys.argv) > 1:
        n_client = int(sys.argv[1])

    input_thread = threading.Thread(target=user_input_thread, daemon=True)
    input_thread.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(n_client)

        print(f"> Server {HOST} listening on port {PORT}")
        print("-"*50)
        print()

        while True:
            try:
                client, addr = s.accept()
                client_handler = threading.Thread(target=handle_client, args=(client, addr))
                client_handler.start()
            except KeyboardInterrupt:
                print("> Server shutting down...")
                with connections_lock:
                    for addr, client in list(connections.items()):
                        try:
                            client["socket"].close()
                        except:
                            pass
                    connections.clear()
                break


if __name__ == "__main__":
    main()