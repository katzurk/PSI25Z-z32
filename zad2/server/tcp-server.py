import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f"Server {HOST} listening on port {PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected to {addr}")

                data = conn.recv(1024).decode().strip()
                print(f"Received message: {data}")

                response = f"{datetime.now()}; Received message: {data}"
                conn.send(response.encode())
                print(f"Sent response: {response}")


if __name__ == "__main__":
    main()
