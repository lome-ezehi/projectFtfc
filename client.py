import socket
import os

def show_menu():
    print("\nMenu:")
    print("1. LIST - View available files on the server")
    print("2. DOWNLOAD <filename> - Download a file")
    print("3. UPLOAD - Upload a file of your choice")
    print("4. HELP - Show this help message")
    print("5. EXIT - Close connection")

def list_local_files(directory):
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if files:
            print("\nAvailable files in your directory:")
            for i, file in enumerate(files, 1):
                print(f"{i}. {file}")
            return files
        else:
            print("No files found in the specified directory.")
            return []
    except Exception as e:
        print(f"Error accessing directory: {e}")
        return []

def connect_to_server(host, port):
    s = socket.socket()
    s.connect((host, port))
    print(f"Connected to {host}:{port}")
    
    # Create the 'received' directory if it doesn't exist
    if not os.path.exists('received'):
        os.makedirs('received')
    
    while True:
        show_menu()
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            # Request the list of files from the server
            s.send(b"LIST")
            response = s.recv(4096).decode()
            if response:
                print("\nFiles on the server:")
                print(response)  # Display the list of files from the server
            else:
                print("No files available on the server.")
        
        elif choice == "2":
            # Step 1: Request the list of files from the server
            s.send(b"LIST")
            response = s.recv(4096).decode()
            
            if response:
                print("\nAvailable files on the server:")
                files = response.split("\n")
                for i, file in enumerate(files, 1):
                    print(f"{i}. {file}")

                # Step 2: Prompt user to select a file
                file_index = input("Enter the number of the file to download: ").strip()
                
                if file_index.isdigit() and 1 <= int(file_index) <= len(files):
                    filename = files[int(file_index) - 1]
                    s.send(f"DOWNLOAD {filename}".encode())  # Send download request
                    
                    # Step 3: Wait for the server to respond
                    response = s.recv(1024).decode()
                    if response.startswith("OK"):
                        file_size = int(response.split()[1])
                        received_path = os.path.join("received", filename)
                        
                        # Step 4: Start receiving the file in chunks
                        with open(received_path, "wb") as file:
                            while file_size > 0:
                                data = s.recv(min(1024, file_size))
                                file.write(data)
                                file_size -= len(data)
                        print(f"File '{filename}' downloaded successfully to 'received' directory.")
                    else:
                        print("Error: File not found on the server.")
                else:
                    print("Invalid selection.")
            else:
                print("No files available on the server.")
        
        elif choice == "3":
            directory = "./"  # Change this to a specific folder if needed
            files = list_local_files(directory)
            if files:
                file_index = input("Enter the number of the file to upload: ").strip()
                if file_index.isdigit() and 1 <= int(file_index) <= len(files):
                    filename = files[int(file_index) - 1]
                    file_path = os.path.join(directory, filename)
                    file_size = os.path.getsize(file_path)
                    
                    # Send upload command to the server
                    s.send(f"UPLOAD {filename} {file_size}".encode())
                    response = s.recv(1024).decode()
                    
                    if response == "READY":
                        with open(file_path, "rb") as file:
                            while (data := file.read(1024)):
                                s.send(data)  # Send the file in chunks
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
                                s.send(f"RENAME {new_name}".encode())
                                response = s.recv(1024).decode()
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
            help_message = s.recv(1024).decode()
            print(help_message)  # Display the help message
        
        elif choice == "5":
            s.send(b"EXIT")
            print("Closing connection...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
    
    s.close()

if __name__ == "__main__":
    connect_to_server("127.0.0.1", 2389)
