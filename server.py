import socket
import os

def handle_client(conn):
    while True:
        command = conn.recv(1024).decode().strip()
        if not command:
            continue

        if command == "LIST":
            # List files in the 'uploads' directory
            files = os.listdir("uploads")
            if files:
                conn.send("\n".join(files).encode())  # Send the list of files
            else:
                conn.send(b"No files available.")

        elif command.startswith("DOWNLOAD"):
            _, filename = command.split(" ", 1)
            download_path = os.path.join("uploads", filename)
            
            # Check if the requested file exists
            if os.path.exists(download_path):
                file_size = os.path.getsize(download_path)
                conn.send(f"OK {file_size}".encode())  # Send OK response and file size
                
                # Sending the file in chunks
                with open(download_path, "rb") as file:
                    while (data := file.read(1024)):
                        conn.send(data)
                print(f"File '{filename}' sent successfully.")
            else:
                conn.send(b"ERROR File not found.")  # File not found response
        
        elif command == "HELP":
            help_message = """
Help Guide:
1. LIST: Displays all the files available on the server.
2. DOWNLOAD <filename>: Downloads the specified file from the server.
3. UPLOAD: Upload a file from your local machine to the server.
4. EXIT: Close the connection with the server.
            """
            conn.send(help_message.encode())  # Send help message to client
        
        elif command == "EXIT":
            print("Client disconnected.")
            break

    conn.close()

def start_server(host, port):
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        conn, addr = s.accept()
        print(f"Connection established with {addr}")
        handle_client(conn)

if __name__ == "__main__":
    start_server("127.0.0.1", 2389)
