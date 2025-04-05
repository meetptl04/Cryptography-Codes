import socket
from helper import playfair_encrypt  # Import Playfair functions

def client():
    s = socket.socket()
    s.connect(('localhost', 8080))
    key = input("Enter the Key : ")
    msg = input("Enter message: ")
    encrypted = playfair_encrypt(msg, key)
    print(f"Encrypted: {encrypted}")
    s.send(key.encode())
    s.send(encrypted.encode())
    s.close()

client()
