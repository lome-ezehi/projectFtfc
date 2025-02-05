import socket
import os

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def handle_client(conn, addr):
    print(f"Connected with {addr}")

    while True:
        command = conn.recv(1024).decode('utf-8').strip()
        if not command:
            continue

        # TODO : List
        if command == "LIST":
            files = os.listdir(UPLOAD_DIR)
            conn.send("\n".join(files).encode('utf-8') if files else b"No files available.")

        # TODO : Download
        elif command.startswith("DOWNLOAD"):
            _, filename = command.split(" ", 1)
            file_path = os.path.join(UPLOAD_DIR, filename)
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                conn.send(f"OK {file_size}".encode('utf-8'))
                with open(file_path, "rb") as file:
                    while (data := file.read(1024)):
                        conn.send(data)
                print(f"File '{filename}' sent to {addr}.")
            else:
                conn.send(b"ERROR File not found.")

        # TODO : Upload
        elif command.startswith("UPLOAD"):
            _, filename, file_size = command.split(" ", 2)
            file_size = int(file_size)
            file_path = os.path.join(UPLOAD_DIR, filename)

            if os.path.exists(file_path):
                conn.send(b"EXISTS")
            else:
                conn.send(b"READY")
                with open(file_path, "wb") as file:
                    while file_size > 0:
                        data = conn.recv(min(1024, file_size))
                        file.write(data)
                        file_size -= len(data)
                print(f"File '{filename}' uploaded from {addr}.")

        # TODO : Help
        elif command == "HELP":
            help_message = """\nCommands:\nLIST - View files\nDOWNLOAD <filename> - Get file\nUPLOAD <filename> - Send file\nEXIT - Disconnect"""
            conn.send(help_message.encode('utf-8'))

        # TODO : Exit
        elif command == "EXIT":
            print(f"Client {addr} disconnected.")
            break

    conn.close()

def start_server():
    host = input("Enter server host (default: 0.0.0.0): ").strip() or "0.0.0.0"
    port = int(input("Enter server port (default: 2389): ").strip() or 2389)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        conn, addr = s.accept()
        handle_client(conn, addr)

if __name__ == "__main__":
    start_server()
