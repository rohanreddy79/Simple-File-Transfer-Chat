import socket
import threading

BUFFER_SIZE = 4096

def handle_write(sock, sender_name):
    while True:
        message = input()
        command = f"{sender_name}: {message}"
        sock.send(command.encode())

        if message.startswith("transfer"):
            _, filename = message.split(" ", 1)
            sock.sendall(f"FILE_START {filename}".encode())
            with open(filename, "rb") as file:
                file_data = file.read(BUFFER_SIZE)
                while file_data:
                    sock.sendall(file_data)
                    file_data = file.read(BUFFER_SIZE)
            sock.sendall(b"FILE_END")
        if message == "exit":
            break

    sock.close()

def handle_read(sock):
    receiving_file = False
    file_data = bytearray()
    filename = ""

    while True:
        data = sock.recv(BUFFER_SIZE)
        if not data:
            break

        if data.startswith(b"FILE_START"):
            filename = data.split(b" ")[-1].decode('latin-1').strip()
            receiving_file = True
            file_data = bytearray()
        else:
            if receiving_file:
                if data.endswith(b"FILE_END"):
                    data = data[:-8]
                    receiving_file = False
                file_data.extend(data)
                if not receiving_file:
                    new_filename = f"new_{filename}"
                    with open(new_filename, "wb") as file:
                        file.write(file_data)
                    file_data = bytearray()
                    filename = ""
            else:
                try:
                    message = data.decode()
                    print(message)
                    if message == "exit":
                        break
                except UnicodeDecodeError:
                    receiving_file = True
                    file_data.extend(data)

    sock.close()

def main():
    sender_name = input("Enter your name: ")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", 0))
    server_socket.listen(1)
    print(f"Listening on port: {server_socket.getsockname()[1]}")

    target_port = int(input("Enter target port: "))
    writing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    writing_socket.connect(("localhost", target_port))

    writing_thread = threading.Thread(target=handle_write, args=(writing_socket, sender_name))
    writing_thread.start()

    conn, _ = server_socket.accept()
    print("Connection established")

    reading_thread = threading.Thread(target=handle_read, args=(conn,))
    reading_thread.start()

    writing_thread.join()
    reading_thread.join()

if __name__ == "__main__":
    main()
