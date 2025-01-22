import socket
import argparse
import os

def receive_file(host, port):
    s = socket.socket()

    try:
        s.connect((host, port))
        print(f"Connected to the server at {host}:{port}.")

        filename = input("Enter the filename to save the file as: ")
        folder = "received"
        os.makedirs(folder, exist_ok=True)  # Ensure the 'received' folder exists
        filepath = os.path.join(folder, filename)

        # Check if the file already exists
        if os.path.exists(filepath):
            print(f"File '{filename}' already exists in the 'received' folder.")
            while True:
                choice = input("Do you want to overwrite (O), rename (R), or cancel (C)? ").strip().lower()
                if choice == 'o':  # Overwrite
                    print(f"Overwriting the file '{filename}'.")
                    break
                elif choice == 'r':  # Rename
                    new_name = input("Enter a new filename: ").strip()
                    filepath = os.path.join(folder, new_name)
                    print(f"Saving as '{new_name}'.")
                    break
                elif choice == 'c':  # Cancel
                    print("Operation canceled.")
                    s.close()
                    return
                else:
                    print("Invalid choice. Please enter 'O', 'R', or 'C'.")

        # Receive and save the file
        with open(filepath, "wb") as file:
            while True:
                file_data = s.recv(1024)
                if not file_data:
                    break
                file.write(file_data)
        print(f"File received and saved as '{filepath}'.")
    except ConnectionError:
        print("Error: Unable to connect to the server.")
    finally:
        s.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Receive a file from the server.")
    parser.add_argument("--host", type=str, required=True, help="Host address of the server.")
    parser.add_argument("--port", type=int, default=9999, help="Port number to connect to (default: 9999).")
    args = parser.parse_args()

    receive_file(args.host, args.port)
