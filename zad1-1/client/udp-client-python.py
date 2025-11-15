import socket
import sys

HOST = "z32-server-c"
PORT = 5550
BUFSIZE = 1024

def main():
    host = HOST
    port = PORT

    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    print(f"Connecting to {host} on port {port}...")
    addr = (host, port)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            msg = b"Test datagram"

            print(f"Sending datagram to server - size: {len(msg)} bytes")
            s.sendto(msg, addr)

            data = s.recv(BUFSIZE)
            print(f"Received response from server: {data}")

        except Exception as e:
            print("Error:", e)

    print("Disconnected")

if __name__ == "__main__":
    main()