import socket
import argparse
import os
import struct  # For packing file size into bytes

def start_server(host, port):
    s = socket.socket()
    s.bind((host, port))
    s.listen(1)
    print(f"Server started on {host}:{port}")
    print("Waiting for a connection...")

    conn, addr = s.accept()
    print(f"Connection established with {addr}")

    while True:
        filenames = input("Enter filenames to send (separated by commas): ").strip()
        filenames_list = [filename.strip() for filename in filenames.split(",")]

        missing_files = [file for file in filenames_list if not os.path.isfile(file)]
        if missing_files:
            print(f"Error: The following files were not found: {', '.join(missing_files)}")
            continue

        conn.send(",".join(filenames_list).encode())  # Send filenames
        print(f"Filenames sent to the client: {', '.join(filenames_list)}")
        break

    for filename in filenames_list:
        try:
            file_size = os.path.getsize(filename)
            """
            The file size is sent to the client to let it know how many bytes it should expect for this file.
            struct.pack("!Q", file_size):
                !: Network byte order (big-endian).
                Q: An unsigned 8-byte integer (enough to store very large file sizes, up to ~18 exabytes).
                This ensures the file size is sent as a fixed-length 8-byte number, regardless of the actual file size.
            """
            conn.send(struct.pack("!Q", file_size))  # Send file size as 8-byte big-endian unsigned integer

            with open(filename, "rb") as file:
                print(f"Sending file: {filename}")
                #Walrus operator(:=) assigns and breaks out once empty
                while (data := file.read(1024)):  # Send in chunks
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
