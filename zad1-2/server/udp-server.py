import socket

HOST = "0.0.0.0"
PORT = 5000
BUFSIZE = 1024


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"UDP server {HOST} listening on port {PORT}")

        while True:
            data, addr = s.recvfrom(BUFSIZE)
            message = data.decode().strip()
            print(f"Received mesage: {message}\n from address: {addr}")


if __name__ == "__main__":
    main()
