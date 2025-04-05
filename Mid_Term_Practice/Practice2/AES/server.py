import socket
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Function to decrypt using AES
def aes_decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_text = unpad(cipher.decrypt(bytes.fromhex(ciphertext)), AES.block_size).decode()
    return decrypted_text

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)

    print("Server is waiting for connection...")
    client_socket, client_addr = server_socket.accept()
    print(f"Client connected from: {client_addr}")

    # Receive key and encrypted message
    data = json.loads(client_socket.recv(1024).decode())
    key = data["key"].encode()
    encrypted_msg = data["message"]

    print(f"Received Encrypted: {encrypted_msg}")

    decrypted_msg = aes_decrypt(encrypted_msg, key)
    print(f"Decrypted Message: {decrypted_msg}")

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    server()
