import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import socket
import os
import threading

# Global Variables
server_socket = None
conn = None
addr = None

def start_server():
    global server_socket, conn, addr

    def server_thread():
        try:
            host = "127.0.0.1"
            port = 9999
            server_socket = socket.socket()
            server_socket.bind((host, port))
            server_socket.listen(1)
            status_text.set(f"Server started at {host}:{port}")
            status_label.config(bg="lightgreen")  # Success background
            conn, addr = server_socket.accept()
            status_text.set(f"Connected with {addr}")
            status_label.config(bg="green")  # Connected background
        except Exception as e:
            status_text.set("Failed to start server.")
            status_label.config(bg="red")  # Error background
            messagebox.showerror("Error", f"Failed to start server: {e}")

    # Run the server in a separate thread
    threading.Thread(target=server_thread, daemon=True).start()

def send_files():
    global conn
    if conn is None:
        messagebox.showerror("Error", "No client is connected.")
        return

    try:
        filenames = filedialog.askopenfilenames(title="Select Files to Send")
        if not filenames:
            return  # No files selected

        for filename in filenames:
            conn.send(os.path.basename(filename).encode())
            conn.recv(1024)  # Wait for acknowledgment

            with open(filename, "rb") as file:
                while chunk := file.read(1024):
                    conn.send(chunk)
            conn.send(b"EOF")  # End of file marker

        status_text.set("Files sent successfully.")
        status_label.config(bg="green")  # Success background
    except Exception as e:
        status_text.set("Error: Failed to send files.")
        status_label.config(bg="red")  # Error background
        messagebox.showerror("Error", f"Failed to send files: {e}")
    finally:
        conn.close()
        server_socket.close()

# Tkinter GUI
app = tk.Tk()
app.title("File Transfer Server")
app.geometry("500x400")
app.resizable(False, False)

status_text = tk.StringVar()
status_text.set("Status: Waiting to start server")


# Header Section
header_frame = tk.Frame(app, bg="#fff")
header_frame.pack(fill="x")
tk.Label(header_frame, text="File Transfer Server", bg="#fff", fg="black", font=("Helvetica", 22, "bold")).pack(pady=7)

# Control Buttons
button_frame = tk.Frame(app)
button_frame.pack(pady=20)
start_button = ttk.Button(button_frame, text="Start Server", command=start_server)
start_button.grid(row=0, column=0, padx=10)
send_button = ttk.Button(button_frame, text="Send Files", command=send_files)
send_button.grid(row=0, column=1, padx=10)

# Status Section
status_frame = tk.Frame(app, bg="#f4f4f4", relief="sunken", borderwidth=1)
status_frame.pack(fill="x", padx=0, pady=10)
status_label = tk.Label(status_frame, textvariable=status_text, bg="black", anchor="w")
# status_label.grid(row=0, column=0, padx=10)
status_label.pack(fill="x", padx=5, pady=5)

app.mainloop()
