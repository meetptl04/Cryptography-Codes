import socket
import json

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)
    print("Yeah I am Server : Hahahaha")

    client_socket, client_addr = server_socket.accept()
    print(f"Client is Connected at: {client_addr}")

    shift = int(client_socket.recv(1024).decode())  # Receive shift value
    encrypted = client_socket.recv(1024).decode()  # Receive encrypted text

    msg = ""
    shift = -shift  # Reverse the shift for decryption
    for char in encrypted:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')  # Correct base
            msg += chr((ord(char) - base + shift) % 26 + base)
        else:
            msg += char  # Keep non-alphabet characters unchanged

    print(f"Message is: {msg}")

    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    server()
