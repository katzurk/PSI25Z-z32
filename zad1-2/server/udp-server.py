import socket

HOST = "0.0.0.0"
PORT = 5000
BUFSIZE = 1024


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"UDP server listening on {PORT}")

        while True:
            data, addr = s.recvfrom(BUFSIZE)

            seq_num = data[0]
            payload = data[1:]

            print(f"Packet from {addr}: Seq={seq_num}, Payload Size={len(payload)} bytes")

            ack = bytes([seq_num])
            s.sendto(ack, addr)


if __name__ == "__main__":
    main()