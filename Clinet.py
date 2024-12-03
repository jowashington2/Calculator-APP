import socket

# Replace with your Render-assigned server IP or domain
server_ip = "your-app-name.onrender.com"  # Use the Render-provided domain
server_port = 12345  # Replace with the assigned port

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Ask the user for a number to send
number = int(input("Enter a number to get the Fibonacci sum (or -1 to shut down the server): "))
client_socket.sendall(str(number).encode())

# Receive and print the result
result = client_socket.recv(1024).decode()
print(f"Result from server: {result}")

client_socket.close()
