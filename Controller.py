import socket
import threading
import json

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            task = eval(data)  # Deserialize task (simplistic approach, use JSON in production)
            user_id = task["user_id"]
            task_data = task["task"]

            if task_data["type"] == "2":  # Fibonacci Task
                result = send_to_fibonacci_worker(task_data["data"])
                response = f"Result for User {user_id}: {result}"
            else:
                response = "Unsupported task type."

            client_socket.sendall(response.encode())
        except Exception as e:
            print(f"Error handling client: {e}")
            break

def send_to_fibonacci_worker(n):
    # Connect to Fibonacci Worker
    worker_ip = '127.0.0.1'  # Worker server IP (adjust as needed)
    worker_port = 9090

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as worker_socket:
        worker_socket.connect((worker_ip, worker_port))
        worker_socket.sendall(str(n).encode())
        result = worker_socket.recv(1024).decode()
    return result

def start_server():
    server_ip = '192.168.0.77'  # Updated to bind to your active interface
    server_port = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_ip, server_port))
        server_socket.listen(5)
        print(f"Server is running on {server_ip}:{server_port} and listening for connections...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            threading.Thread(target=handle_client, args=(client_socket,)).start()

start_server()
