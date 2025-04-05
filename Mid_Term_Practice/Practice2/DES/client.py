import socket
from Crypto.Cipher import DES
import json

# Function to pad text to be a multiple of 8 bytes
def pad(text):
    while len(text) % 8 != 0:
        text += " "
    return text

# Function to encrypt using DES
def des_encrypt(plaintext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    padded_text = pad(plaintext)
    encrypted_text = cipher.encrypt(padded_text.encode()).hex()
    return encrypted_text

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    key = input("Enter 8-character key (must be exactly 8 characters): ").encode()
    message = input("Enter the message to encrypt: ")

    encrypted_msg = des_encrypt(message, key)

    print(f"Encrypted Text: {encrypted_msg}")

    data = json.dumps({"key": key.decode(), "message": encrypted_msg})
    client_socket.send(data.encode())

    client_socket.close()

if __name__ == "__main__":
    client()
