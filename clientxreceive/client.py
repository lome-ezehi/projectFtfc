import tkinter as tk
from tkinter import filedialog, ttk
import socket
import os

def connect_to_server():
    host = host_entry.get()
    port = int(port_entry.get())

    try:
        client_socket.connect((host, port))
        status_text.set(f"Connected to server at {host}:{port}")
        status_label.config(bg="green")  # Success background
    except ConnectionError:
        status_text.set("Error: Could not connect to server.")
        status_label.config(bg="red")  # Error background

def receive_files():
    try:
        folder = filedialog.askdirectory(title="Select Folder to Save Files")
        if not folder:
            status_text.set("File download canceled.")
            status_label.config(bg="#f4f4f4")  # Reset background
            return

        while True:
            filename = client_socket.recv(1024).decode()
            if not filename:
                break
            
            file_path = os.path.join(folder, filename)
            with open(file_path, "wb") as file:
                while True:
                    file_data = client_socket.recv(1024)
                    if file_data == b"EOF":  # End of file marker
                        break
                    file.write(file_data)

            status_text.set(f"File received: {filename}")
            status_label.config(bg="green")  # Success background
    except Exception as e:
        status_text.set(f"Error: {str(e)}")
        status_label.config(bg="red")  # Error background
    finally:
        client_socket.close()

# Tkinter GUI
app = tk.Tk()
app.title("File Transfer Client")
app.geometry("500x400")
app.resizable(False, False)

status_text = tk.StringVar()
status_text.set("Status: Not connected")

# Header Section
header_frame = tk.Frame(app, bg="#fff")
header_frame.pack(fill="x")
tk.Label(header_frame, text="File Transfer Client", bg="#fff", fg="black", font=("Helvetica", 22, "bold")).pack(pady=7)

# Connection Section
connection_frame = tk.Frame(app)
connection_frame.pack(pady=20)
tk.Label(connection_frame, text="Server Host:").grid(row=0, column=0, pady=5, sticky="e")
host_entry = ttk.Entry(connection_frame)
host_entry.insert(0, "127.0.0.1")
host_entry.grid(row=0, column=1, pady=5)

tk.Label(connection_frame, text="Server Port:").grid(row=1, column=0, pady=5, sticky="e")
port_entry = ttk.Entry(connection_frame)
port_entry.insert(0, "9999")
port_entry.grid(row=1, column=1, pady=5)

connect_button = ttk.Button(connection_frame, text="Connect", command=connect_to_server)
connect_button.grid(row=2, column=0, columnspan=2, pady=10)

# Action Buttons
action_frame = tk.Frame(app)
action_frame.pack(pady=10)
download_button = ttk.Button(action_frame, text="Download Files", command=receive_files)
download_button.pack()

# Status Section
status_frame = tk.Frame(app, bg="#f4f4f4", relief="sunken", borderwidth=1)
status_frame.pack(fill="x", padx=10, pady=10)
status_label = tk.Label(status_frame, textvariable=status_text, bg="black", anchor="w")
status_label.pack(fill="x", padx=5, pady=5)

client_socket = socket.socket()
app.mainloop()
