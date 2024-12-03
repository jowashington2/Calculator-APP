import socket
import threading

# Fibonacci calculation function
def fibonacci_sum(n):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

# Function to handle each client connection
def handle_client(client_socket):
    try:
        # Receive the number from the client
        number = int(client_socket.recv(1024).decode())
        
        if number == -1:  # If the number received is -1, initiate server shutdown
            print("Shutdown command received. Closing server.")
            client_socket.sendall("Server is shutting down.".encode())
            client_socket.close()
            server_socket.close()  # Shut down the server socket
            return
        
        # Compute the Fibonacci sum
        result = fibonacci_sum(number)
        
        # Send the result back to the client
        client_socket.sendall(str(result).encode())
    except Exception as e:
        client_socket.sendall(f"Error: {str(e)}".encode())
    finally:
        client_socket.close()

# Function to start the server
def start_server(ip, port):
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print(f"Server listening on {ip}:{port}...")

    while True:
        # Wait for a connection
        client_socket, addr = server_socket.accept()
        print(f"Connection established with {addr}")
        
        # Handle the client in a separate thread
        threading.Thread(target=handle_client, args=(client_socket,)).start()

# Main function to run the server
if __name__ == "__main__":
    server_ip = "0.0.0.0"  # Allow access from any IP address
    server_port = 9090      # The port on which the server will listen
    start_server(server_ip, server_port)
