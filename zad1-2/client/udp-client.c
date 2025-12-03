#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>

#define HOST "z32-server-python"
#define PORT 5000
#define FILE_NAME "random.bin"
#define FILE_SIZE 10000
#define PACKET_DATA_SIZE 100
#define PACKET_SIZE (PACKET_DATA_SIZE + 1)


int load_file(const char *filename, char *buffer, size_t max_size) {
    FILE *file = fopen(filename, "rb");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }
    size_t bytes_read = fread(buffer, 1, max_size, file);
    fclose(file);
    return bytes_read;
}

int main(void) {
    int sock;
    struct sockaddr_in server_addr;
    struct hostent *server;
    char file_buffer[FILE_SIZE];

    if ((load_file(FILE_NAME, file_buffer, FILE_SIZE)) != FILE_SIZE) {
        fprintf(stderr, "Error: Could not read the complete file %s\n", FILE_NAME);
        return 1;
    }

    server = gethostbyname(HOST);
    if (server == NULL) {
        fprintf(stderr, "Error: No such host %s\n", HOST);
        return 1;
    }

    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("Error opening socket");
        return 1;
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    memcpy(&server_addr.sin_addr, server->h_addr_list[0], server->h_length);

    char packet[PACKET_SIZE];
    char current_seq = 0;
    char ack;
    int total_packets = FILE_SIZE / PACKET_DATA_SIZE;
    int i = 0;
    struct timeval timeout;
    int max_retries = 10;

    timeout.tv_sec = 2;
    timeout.tv_usec = 0;
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));

    printf("Starting sending packets in 10s...\n\n");
    sleep(10); // to run disrupt.sh

    while (i < total_packets) {

        packet[0] = current_seq;

        memcpy(&packet[1], &file_buffer[i * PACKET_DATA_SIZE], PACKET_DATA_SIZE);

        sendto(sock, packet, PACKET_SIZE, 0, (struct sockaddr*)&server_addr, sizeof(server_addr));
        printf("Sent Packet %d: Seq=%d\n", i, current_seq);

        int nread = recvfrom(sock, &ack, 1, 0, NULL, NULL);

        if (nread > 0 && ack == current_seq) {
            printf("Received ACK: %d\n", ack);
            current_seq = !current_seq;
            i++;
        }
        else {
            printf("[TIMEOUT] Resending packet %d\n", i);
        }
    }

    printf("Successfully sent all packets\n\n");

    close(sock);
    return 0;
}
