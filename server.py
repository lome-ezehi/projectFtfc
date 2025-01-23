import socket
import argparse
import os

def start_server(host, port):
    s = socket.socket()
    s.bind((host, port))
    s.listen(1)
    print(f"Server started on {host}:{port}")
    print("Waiting for a connection...")

    conn, addr = s.accept()
    print(f"Connection established with {addr}")

    while True:
        filename = input("Enter the filename to send: ")
        if os.path.isfile(filename):  # Check if the file exists
            break # breaks out even if loop is true
        print(f"Error: The file '{filename}' was not found. Please try again.")

    try:
        with open(filename, "rb") as file:
            file_data = file.read(1024)
            while file_data:
                conn.send(file_data)
                file_data = file.read(1024)
        print("The File has been transmitted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
        s.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start a file server.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host address (default: 127.0.0.1).")
    parser.add_argument("--port", type=int, default=9999, help="Port number (default: 9999).")
    args = parser.parse_args()

    start_server(args.host, args.port)
