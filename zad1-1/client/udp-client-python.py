import socket
import sys
from time import time
from matplotlib import pyplot as plt

NO_PACKETS = 17

HOST = "z32-server-c"
PORT = 5550
BUFSIZE = 32768

times_dict = dict()


def main():
    host = HOST
    port = PORT

    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    print(f"Connecting to {host} on port {port}...\n")
    addr = (host, port)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            for i in range(NO_PACKETS):
                msg = b"a"*2**i

                print(f"Sending datagram to server - size: {len(msg)} bytes")
                start = time()
                s.sendto(msg, addr)

                data = s.recv(BUFSIZE)
                times_dict[len(msg)] = time() - start
                print(f"Received response from server: {data}")
                print("-" * 50)

        except Exception as e:
            print("Error:", e)

    print()
    print("Disconnected\n")


if __name__ == "__main__":
    main()

    if times_dict:
        for k, v in times_dict.items():
            print(f"Size: {k} bytes, Round-trip time: {v:.6f} seconds")

    plt.figure(figsize=(10, 6))
    plt.plot(
        list(times_dict.keys()),
        list(times_dict.values()),
        marker='o')
    plt.xscale('log', base=2)
    plt.xlabel('Datagram Size (bytes)')
    plt.ylabel('Round-Trip Time (seconds)')
    plt.grid(True, alpha=0.3)
    plt.savefig('/output/udp_client_rtt.png')
