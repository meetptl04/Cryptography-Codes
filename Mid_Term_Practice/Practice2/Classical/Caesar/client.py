import socket
import json

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))
    print("Yeah I am Client : Hahahaha")

    msg = input("Enter the message (to encrypt using Caesar cipher): ")
    shift = int(input("Enter the shift in number for shifting: "))

    client_socket.send(f"{shift}".encode())  # Send shift value

    result = ""
    for char in msg:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')  # Correct base
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char  # Keep non-alphabet characters unchanged

    print(f"Encrypted Text: {result}")
    client_socket.send(result.encode())  # Send encrypted text as a string

    client_socket.close()

if __name__ == '__main__':
    client()
