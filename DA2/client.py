# client.py - Client-side for encryption and sending data to server
import socket
from enigma_block import encrypt


def client():
    host, port = 'localhost', 12345
    key = 0xA3B1C2D3E4F56789A3B1C2D3E4F56789  # 128-bit key

    plaintext = input("Enter text to encrypt: ")
    ciphertext = encrypt(plaintext, key)

    print("Encrypted (Hex):", ciphertext.hex())

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(ciphertext)
        decrypted_text = s.recv(1024).decode(errors='ignore')

    print("Decrypted at Client:", decrypted_text)


if __name__ == "__main__":
    client()