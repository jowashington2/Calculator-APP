import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Function to send a Fibonacci task to a server
def connect_to_server(ip, port, n, gui_log):
    try:
        # Create a socket and connect to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(str(n).encode())  # Send the Fibonacci task (number n)
            result = s.recv(1024).decode()  # Receive the result
            gui_log.insert(tk.END, f"Sent task to server {ip}:{port} - Result: {result}\n")
            gui_log.see(tk.END)
    except Exception as e:
        gui_log.insert(tk.END, f"Failed to connect to server {ip}:{port}. Error: {str(e)}\n")
        gui_log.see(tk.END)

# GUI setup
def start_gui():
    root = tk.Tk()
    root.title("Fibonacci Worker Client")

    # Text area for logs
    log_frame = tk.Frame(root)
    log_frame.pack(fill=tk.BOTH, expand=True)

    gui_log = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=20, width=80)
    gui_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Server connection frame
    connection_frame = tk.Frame(root)
    connection_frame.pack(pady=10)

    # Server IP address and port entry
    tk.Label(connection_frame, text="Server IP:").grid(row=0, column=0)
    server_ip_entry = tk.Entry(connection_frame, width=30)
    server_ip_entry.grid(row=0, column=1)
    server_ip_entry.insert(tk.END, 'calculator-app-1.onrender.com')  # Default Render domain

    tk.Label(connection_frame, text="Server Port:").grid(row=1, column=0)
    server_port_entry = tk.Entry(connection_frame, width=10)
    server_port_entry.grid(row=1, column=1)
    server_port_entry.insert(tk.END, '12345')  # Replace with your Render server's assigned port

    tk.Label(connection_frame, text="Enter n for Fibonacci sum:").grid(row=2, column=0)
    number_entry = tk.Entry(connection_frame, width=20)
    number_entry.grid(row=2, column=1)

    # Function to handle the button click to connect and send data
    def on_connect():
        ip = server_ip_entry.get()
        port = int(server_port_entry.get())
        try:
            n = int(number_entry.get())
            if n <= 0:
                messagebox.showerror("Invalid Input", "Please enter a positive integer.")
                return
            gui_log.insert(tk.END, f"Connecting to server {ip}:{port} for n={n}...\n")
            gui_log.see(tk.END)
            threading.Thread(target=connect_to_server, args=(ip, port, n, gui_log), daemon=True).start()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer for 'n'.")

    # Connect button
    connect_button = tk.Button(connection_frame, text="Connect and Send Task", command=on_connect)
    connect_button.grid(row=3, column=0, columnspan=2)

    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    start_gui()
