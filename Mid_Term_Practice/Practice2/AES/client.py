import socket
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Function to encrypt using AES
def aes_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_text = pad(plaintext.encode(), AES.block_size)
    encrypted_text = cipher.encrypt(padded_text).hex()
    return encrypted_text

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    key = input("Enter 16-character key (must be exactly 16 characters): ").encode()
    message = input("Enter the message to encrypt: ")

    encrypted_msg = aes_encrypt(message, key)

    print(f"Encrypted Text: {encrypted_msg}")

    data = json.dumps({"key": key.decode(), "message": encrypted_msg})
    client_socket.send(data.encode())

    client_socket.close()

if __name__ == "__main__":
    client()
