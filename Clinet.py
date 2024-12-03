import threading
from flask import Flask, render_template, request
import socket
import time
import os

app = Flask(__name__)

# Fibonacci Calculation
def fibonacci_sum(n):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

# Socket Server to Handle Fibonacci Requests
def start_socket_server():
    server_ip = "0.0.0.0"  # Listen on all interfaces
    server_port = int(os.environ.get("PORT", 9090))  # Use Render's PORT env variable
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print(f"Socket server listening on {server_ip}:{server_port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        try:
            data = int(client_socket.recv(1024).decode())
            result = fibonacci_sum(data)
            client_socket.sendall(str(result).encode())
        except Exception as e:
            client_socket.sendall(f"Error: {str(e)}".encode())
        finally:
            client_socket.close()

# Flask Endpoint
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    elapsed_time = None

    if request.method == "POST":
        try:
            n = int(request.form["n"])
            start_time = time.time()
            # Connect to the local socket server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(("127.0.0.1", 9090))  # Connect to the local socket server
                client_socket.sendall(str(n).encode())
                result = client_socket.recv(1024).decode()
            elapsed_time = round(time.time() - start_time, 4)
        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template("index.html", result=result, elapsed_time=elapsed_time, error=error)

if __name__ == "__main__":
    # Start the socket server in a separate thread
    threading.Thread(target=start_socket_server, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
