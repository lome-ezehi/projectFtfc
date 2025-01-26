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

    # Step 1: Prompt the user for filenames
    while True:
        filenames = input("Enter filenames to send (separated by commas): ").strip()
        filenames_list = [filename.strip() for filename in filenames.split(",")]

        # Check if all files exist
        missing_files = [file for file in filenames_list if not os.path.isfile(file)]
        if missing_files:
            print(f"Error: The following files were not found: {', '.join(missing_files)}")
            continue

        # Send filenames list to the client
        conn.send(",".join(filenames_list).encode())
        print(f"Filenames sent to the client: {', '.join(filenames_list)}")
        break

    # Step 2: Send each file
    for filename in filenames_list:
        try:
            with open(filename, "rb") as file:
                print(f"Sending file: {filename}")
                while (data := file.read(1024)):  # Read and send data in chunks
                    conn.send(data)
            print(f"File '{filename}' sent successfully.")
        except Exception as e:
            print(f"Error sending file '{filename}': {e}")

    conn.close()
    s.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start a file server.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host address (default: 127.0.0.1).")
    parser.add_argument("--port", type=int, default=9999, help="Port number (default: 9999).")
    args = parser.parse_args()

    start_server(args.host, args.port)
