import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000

def send(conn, message):
    conn.sendall(message.encode())
    print(f"Sent message: {message}")

def receive(conn):
    data = conn.recv(1024).decode().strip()
    print(f"Received message: {data}")
    return data


def perform_operation(num1, num2, operation):
    if operation == '+':
        return num1 + num2
    elif operation == '-':
        return num1 - num2
    elif operation == '*':
        return num1 * num2
    elif operation == '/':
        if num2 != 0:
            return num1 / num2
        else:
            return "Error: Division by zero"
    else:
        return "Error: Unknown operation"

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f"Server {HOST} listening on port {PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected to {addr}")

                num1 = receive(conn)
                send(conn, "received")
                operation = receive(conn)
                send(conn, "received")
                num2 = receive(conn)
                
                print(f"Operation to perform: {num1} {operation} {num2}")
                sum_result = perform_operation(float(num1), float(num2), operation)
                send(conn, f"Result: {sum_result}")


if __name__ == "__main__":
    main()
