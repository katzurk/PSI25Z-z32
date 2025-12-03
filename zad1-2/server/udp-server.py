import socket

HOST = "0.0.0.0"
PORT = 5000
BUFSIZE = 1024
N_PACKETS = 100


def main():
    seq_expected = 0
    recv_packets = 0

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"UDP server listening on {PORT}\n")

        while True:
            data, addr = s.recvfrom(BUFSIZE)

            seq_recv = data[0]
            payload = data[1:]

            if seq_recv == seq_expected:
                print(f"Packet {recv_packets} from {addr}: Seq={seq_recv}, Payload Size={len(payload)} bytes")
                seq_expected = 1 - seq_expected
                recv_packets += 1;
            else:
                print("Duplicated data. Resending ACK")

            ack = bytes([seq_recv])
            s.sendto(ack, addr)
            print(f"Sent ACK: {ack[0]}")

            if recv_packets == N_PACKETS:
                print("Received all packets\n")
                break


if __name__ == "__main__":
    main()