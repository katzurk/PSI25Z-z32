#include <stdio.h>
#include <netdb.h>

#define HOST "z32-server-python"
#define PORT 5000

static int send_message(int sock, const char *msg, size_t len)
{
    ssize_t sent = send(sock, msg, strlen(msg), 0);
    if (sent < 0) {
        perror("Error sending");
        return -1;
    }
    printf("Sent message to server: %s\n", msg);
    return (int)sent;
}


static int recv_message(int sock, char *buf, size_t buf_size)
{
    ssize_t nread = recv(sock, buf, buf_size - 1, 0);
    if (nread < 0) {
        perror("Error receiving");
        return -1;
    }
    if (nread == 0) {
        perror("Server closed connection");
        buf[0] = '\0';
        return -1;
    }

    buf[nread] = '\0';
    printf("Received message from server: %s\n", buf);
    return (int)nread;
}


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

    char num1[64], num2[64], op[8];
    printf("Enter first number: ");
    scanf("%63s", num1);
    if (send_message(sock, num1, strlen(num1)) < 0) { close(sock); return 1; }
    if (recv_message(sock, response, sizeof response) < 0) { close(sock); return 1; }
    printf("Enter operator (+ - * /): ");
    scanf("%7s", op);
    if (send_message(sock, op, strlen(op)) < 0) { close(sock); return 1; }
    if (recv_message(sock, response, sizeof response) < 0) { close(sock); return 1; }

    printf("Enter second number: ");
    scanf("%63s", num2);
    if (send_message(sock, num2, strlen(num2)) < 0) { close(sock); return 1; }
    if (recv_message(sock, response, sizeof response) < 0) { close(sock); return 1; }

    close(sock);
    return 0;
}