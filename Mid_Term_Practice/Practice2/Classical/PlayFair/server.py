import socket
from helper import playfair_decrypt  # Import Playfair functions

def server():
    s = socket.socket()
    s.bind(('localhost', 8080))
    s.listen(1)
    c, _ = s.accept()
    key = c.recv(1024).decode()
    encrypted = c.recv(1024).decode()
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {playfair_decrypt(encrypted, key)}")
    c.close()
    s.close()

server()
