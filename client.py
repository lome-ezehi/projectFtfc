import socket
import argparse
import os
import struct
from tqdm import tqdm  # Progress bar library

def receive_file(host, port):
    s = socket.socket()

    try:
        s.connect((host, port))
        print(f"Connected to the server at {host}:{port}.")

        filenames = s.recv(1024).decode()  # Receive filenames
        if not filenames:
            print("No filenames received.")
            return
        
        filenames_list = filenames.split(",")
        print(f"Filenames received: {', '.join(filenames_list)}")

        for filename in filenames_list:
            folder = "received"
            os.makedirs(folder, exist_ok=True)
            filepath = os.path.join(folder, filename)

            if os.path.exists(filepath):
                print(f"File '{filename}' already exists in the 'received' folder.")
                while True:
                    choice = input("Do you want to overwrite (O), rename (R), or cancel (C)? ").strip().lower()
                    if choice == 'o':
                        break
                    elif choice == 'r':
                        new_name = input("Enter a new filename: ").strip()
                        filepath = os.path.join(folder, new_name)
                        break
                    elif choice == 'c':
                        print("Operation canceled.")
                        return
                    else:
                        print("Invalid choice. Please enter 'O', 'R', or 'C'.")

            file_size_data = s.recv(8)  # Receive 8-byte file size
            file_size = struct.unpack("!Q", file_size_data)[0]  # Unpack size

            print(f"Receiving file '{filename}' of size {file_size} bytes.")
            received_size = 0

            with open(filepath, "wb") as file:
                # Initialize tqdm progress bar
                with tqdm(total=file_size, unit="B", unit_scale=True, desc=f"Downloading {filename}") as progress:
                    while received_size < file_size:
                        data = s.recv(min(1024, file_size - received_size))  # Receive in chunks
                        if not data:
                            break
                        file.write(data)
                        received_size += len(data)
                        progress.update(len(data))  # Update progress bar

            print(f"File received and saved as '{filepath}'.")
    except ConnectionError:
        print("Error: Unable to connect to the server.")
    finally:
        s.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Receive files from the server.")
    parser.add_argument("--host", type=str, required=True, help="Host address of the server.")
    parser.add_argument("--port", type=int, default=9999, help="Port number to connect to (default: 9999).")
    args = parser.parse_args()

    receive_file(args.host, args.port)
