#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>

#define HOST "z32-server-python"
#define PORT 5000
#define DATA "test"

int main(void) {
    int sock;
    struct sockaddr_in server_addr;
    struct hostent *server;

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


    if (sendto(sock, DATA, strlen(DATA), 0, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("Error sending datagram");
        close(sock);
        return 1;
    }

    printf("Sent UDP datagram: %s\n", DATA);

    close(sock);
    return 0;
}
