import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000

def send_message(conn, message):
    try:
        conn.sendall(message.encode())
        print(f"Sent message: {message}")
    except Exception as e:
        print(f"Error sending message: {e}")
        return False
    return True

def recv_message(conn):
    data = conn.recv(1024).decode().strip()
    print(f"Received message: {data}")
    if not data:
        print("No data received, closing connection.")
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

                num1 = recv_message(conn)
                if not num1:
                    continue
                if not send_message(conn, "received first number"):
                    continue
                operation = recv_message(conn)
                if not operation:
                    continue
                if not send_message(conn, "received operator"):
                    continue
                num2 = recv_message(conn)
                if not num2:
                    continue
                if not send_message(conn, "received second number"):
                    continue
                
                print(f"Operation to perform: {num1} {operation} {num2}")
                sum_result = perform_operation(float(num1), float(num2), operation)
                send_message(conn, f"Result: {sum_result}")

if __name__ == "__main__":
    main()
