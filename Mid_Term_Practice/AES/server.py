import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad

def decrypt(ciphertext, key):
    iv = ciphertext[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext[16:]), AES.block_size)

key = get_random_bytes(16)  # 128-bit key
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 12345))
server.listen(1)

print("Server waiting...")
client, addr = server.accept()
client.send(key)

while True:
    ciphertext = client.recv(1024)
    if not ciphertext:
        break
    plaintext = decrypt(ciphertext, key)
    print(f"Received: {plaintext.decode()}")

client.close()
server.close()
