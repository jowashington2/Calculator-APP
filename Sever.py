import socket
import threading
import os
import json
from sympy import symbols, diff, integrate

# Fibonacci calculation function
def fibonacci_sum(n):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

# Additional operations
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        raise ValueError("Division by zero is not allowed.")
    return x / y

def calculus(operation, expression, variable, value=None):
    x = symbols(variable)
    expr = eval(expression)  # Evaluate the expression with sympy symbols
    if operation == "differentiate":
        return str(diff(expr, x))
    elif operation == "integrate":
        return str(integrate(expr, x))
    elif operation == "evaluate":
        if value is None:
            raise ValueError("A value is required for evaluation.")
        return str(expr.subs(x, value))
    else:
        raise ValueError("Unsupported calculus operation.")

# Function to handle each client connection
def handle_client(client_socket):
    try:
        # Receive the request from the client
        data = client_socket.recv(1024).decode()
        request = json.loads(data)  # Expecting a JSON string

        operation = request["operation"]
        result = None

        # Perform the requested operation
        if operation == "fibonacci":
            n = int(request["n"])
            result = fibonacci_sum(n)
        elif operation == "add":
            x, y = request["x"], request["y"]
            result = add(x, y)
        elif operation == "subtract":
            x, y = request["x"], request["y"]
            result = subtract(x, y)
        elif operation == "multiply":
            x, y = request["x"], request["y"]
            result = multiply(x, y)
        elif operation == "divide":
            x, y = request["x"], request["y"]
            result = divide(x, y)
        elif operation in ["differentiate", "integrate", "evaluate"]:
            expression = request["expression"]
            variable = request["variable"]
            value = request.get("value", None)
            result = calculus(operation, expression, variable, value)
        else:
            result = "Unsupported operation."

        # Send the result back to the client
        client_socket.sendall(json.dumps({"result": result}).encode())
    except Exception as e:
        client_socket.sendall(json.dumps({"error": str(e)}).encode())
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
    server_port = int(os.environ.get("PORT", 9090))
    start_server(server_ip, server_port)
