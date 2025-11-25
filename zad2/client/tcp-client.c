#include <stdio.h>
#include <netdb.h>

#define HOST "z32-server-python"
#define PORT 5000


int main(void) {
    int sock;
    struct sockaddr_in server_addr;
    struct hostent *server;
    char message[128];
    char response[256];

    server = gethostbyname(HOST);
    if (server == NULL) {
        fprintf(stderr, "Error: No such host %s\n", HOST);
        return 1;
    }

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("Error opening socket");
        return 1;
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    memcpy(&server_addr.sin_addr, server->h_addr_list[0], server->h_length);

    if (connect(sock, (struct sockaddr *) &server_addr, sizeof(server_addr)) < 0) {
        perror("Error connecting to the server");
        return 1;
    }

    printf("Connected to server %s:%d\n", HOST, PORT);

    sprintf(message, "This is a test.");
    send(sock, message, strlen(message), 0);
    printf("Sent message to server: %s\n", message);

    int nread = recv(sock, response, sizeof(response) - 1, 0);
    response[nread] = '\0';
    printf("Received response from server: %s\n", response);

    close(sock);
    return 0;
}