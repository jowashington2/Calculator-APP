from flask import Flask, render_template, request
import socket
import time
import os
print("Current working directory:", os.getcwd())
print("Templates directory path:", os.path.join(os.getcwd(), "templates"))

app = Flask(__name__)

# Function to send the request to the server and get the result
def get_fibonacci_sum(n, threads):
    try:
        # Connect to the server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 9090))  # Ensure the server is running on this port

        # Send data (n, threads) to the server
        client.send(f"{n},{threads}".encode())

        # Receive the result from the server
        result = client.recv(1024).decode()

        # Close the connection
        client.close()

        return result
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    elapsed_time = None
    
    if request.method == "POST":
        try:
            # Get values from the form
            n = int(request.form["n"])
            threads = int(request.form["threads"])

            start_time = time.time()  # Start timer
            
            # Call the server and get the Fibonacci sum result
            result = get_fibonacci_sum(n, threads)
            
            end_time = time.time()  # End timer
            elapsed_time = round(end_time - start_time, 4)  # Calculate elapsed time
        except Exception as e:
            error = f"Error: {str(e)}"
    
    return render_template("index.html", result=result, elapsed_time=elapsed_time, error=error)

if __name__ == "__main__":
    app.run(debug=True)
