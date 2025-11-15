#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define HOST "0.0.0.0"
#define PORT 5550
#define BUFSIZE 32768

int main(int argc, char *argv[]) {
    int sock, length;
    struct sockaddr_in addr, client_addr;
    socklen_t client_addr_len = sizeof(client_addr);

    const char* host = HOST;
    int port = PORT;
    char buf[BUFSIZE];

    if (argc > 1) {
        port = atoi(argv[1]);
    }

    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1) {
        perror("Error creating the socket\n");
        exit(1);
    }

    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = inet_addr(host);
    addr.sin_port = htons(port);

    if (bind(sock, (struct sockaddr*) &addr, sizeof(addr)) == -1) {
        perror("Error during binding\n");
        exit(1);
    }

    printf("Server %s is listening on port %d\n", host, port);

    while(1) {
        int nread = recvfrom(sock, buf, BUFSIZE, 0, (struct sockaddr*) &client_addr, &client_addr_len);
        if (nread < 0) {
            continue;
        }

        buf[nread] = '\0';
        printf("Received datagram from %s:%d - %s, size: %d bytes\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port), buf, nread);

        char response[64];
        snprintf(response, sizeof(response), "Received datagram - size: %d bytes", nread);
        printf("Sending response to the client\n");
        sendto(sock, response, strlen(response), 0, (struct sockaddr*) &client_addr, client_addr_len);
    }

    close(sock);
    return 0;
}