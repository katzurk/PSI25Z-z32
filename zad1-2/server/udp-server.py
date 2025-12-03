import socket
import hashlib

HOST = "0.0.0.0"
PORT = 5000
BUFSIZE = 1024
N_PACKETS = 100

def main():
    seq_expected = 0
    recv_packets = 0
    received_data = bytearray()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"UDP server listening on {PORT}\n")

        while True:
            data, addr = s.recvfrom(BUFSIZE)

            seq_recv = data[0]
            payload = data[1:]

            if seq_recv == seq_expected:
                print(f"Packet {recv_packets} from {addr}: Seq={seq_recv}, Payload Size={len(payload)} bytes")
                
                received_data.extend(payload)
                
                seq_expected = 1 - seq_expected
                recv_packets += 1
            else:
                print("Duplicated data. Resending ACK")

            ack = bytes([seq_recv])
            s.sendto(ack, addr)
            # print(f"Sent ACK: {ack[0]}")

            if recv_packets == N_PACKETS:
                print("Received all packets\n")
                break
        
        print("-" * 30)
        md5_hash = hashlib.md5(received_data).hexdigest()
        print(f"Server MD5 Hash: {md5_hash}")
        print("-" * 30)

if __name__ == "__main__":
    main()