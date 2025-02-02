import socket
import os

def show_menu():
    print("\nMenu:")
    print("1. LIST - View available files on the server")
    print("2. DOWNLOAD <filename> - Download a file")
    print("3. UPLOAD - Upload a file")
    print("4. HELP - Show this help message")
    print("5. EXIT - Close connection")

def connect_to_server():
    host = input("Enter server IP (default: 127.0.0.1): ").strip() or "127.0.0.1"
    port = int(input("Enter server port (default: 2389): ").strip() or 2389)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print(f"Connected to {host}:{port}")

    if not os.path.exists('received'):
        os.makedirs('received')

    while True:
        show_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            s.send(b"LIST")
            response = s.recv(4096).decode('utf-8')
            print("\nFiles on the server:\n" + response)

        elif choice == "2":
            s.send(b"LIST")
            response = s.recv(4096).decode('utf-8')
            if response:
                files = response.split("\n")
                for i, file in enumerate(files, 1):
                    print(f"{i}. {file}")

                file_index = input("Enter the number of the file to download: ").strip()
                if file_index.isdigit() and 1 <= int(file_index) <= len(files):
                    filename = files[int(file_index) - 1]
                    s.send(f"DOWNLOAD {filename}".encode('utf-8'))

                    response = s.recv(1024).decode('utf-8')
                    if response.startswith("OK"):
                        file_size = int(response.split()[1])
                        received_path = os.path.join("received", filename)

                        with open(received_path, "wb") as file:
                            while file_size > 0:
                                data = s.recv(min(1024, file_size))
                                file.write(data)
                                file_size -= len(data)
                        print(f"File '{filename}' downloaded successfully.")
                    else:
                        print("Error: File not found on the server.")
                else:
                    print("Invalid selection.")
            else:
                print("No files available on the server.")

        elif choice == "3":
            directory = "./"
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            if files:
                for i, file in enumerate(files, 1):
                    print(f"{i}. {file}")
                file_index = input("Enter the number of the file to upload: ").strip()

                if file_index.isdigit() and 1 <= int(file_index) <= len(files):
                    filename = files[int(file_index) - 1]
                    file_path = os.path.join(directory, filename)
                    file_size = os.path.getsize(file_path)

                    s.send(f"UPLOAD {filename} {file_size}".encode('utf-8'))
                    response = s.recv(1024).decode('utf-8')

                    if response == "READY":
                        with open(file_path, "rb") as file:
                            while (data := file.read(1024)):
                                s.send(data)
                        print(f"File '{filename}' uploaded successfully.")
                    elif response == "EXISTS":
                        print("File already exists on the server. Choose a different name or overwrite.")
                        while True:
                            choice = input("Overwrite (O), Rename (R), Cancel (C): ").strip().lower()
                            if choice == 'o':
                                s.send(b"OVERWRITE")
                                with open(file_path, "rb") as file:
                                    while (data := file.read(1024)):
                                        s.send(data)
                                print(f"File '{filename}' overwritten successfully.")
                                break
                            elif choice == 'r':
                                new_name = input("Enter new filename: ").strip()
                                s.send(f"RENAME {new_name}".encode('utf-8'))
                                response = s.recv(1024).decode('utf-8')
                                if response == "READY":
                                    with open(file_path, "rb") as file:
                                        while (data := file.read(1024)):
                                            s.send(data)
                                    print(f"File '{new_name}' uploaded successfully.")
                                    break
                                else:
                                    print("Error renaming file.")
                            elif choice == 'c':
                                print("Upload canceled.")
                                s.send(b"CANCEL")
                                break
                            else:
                                print("Invalid choice. Please enter 'O', 'R', or 'C'.")
                    else:
                        print("Error: Server not ready to receive file.")
                else:
                    print("Invalid selection.")

        elif choice == "4":
            s.send(b"HELP")
            help_message = s.recv(1024).decode('utf-8')
            print(help_message)

        elif choice == "5":
            s.send(b"EXIT")
            print("Closing connection...")
            break
        else:
            print("Invalid choice. Enter a number between 1 and 5.")

    s.close()

if __name__ == "__main__":
    connect_to_server()
