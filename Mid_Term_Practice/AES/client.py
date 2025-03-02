import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.iv + cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return ciphertext

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))
key = client.recv(16)

while True:
    message = input("Enter message (or 'quit' to exit): ")
    if message.lower() == 'quit':
        break
    ciphertext = encrypt(message, key)
    client.send(ciphertext)

client.close()
