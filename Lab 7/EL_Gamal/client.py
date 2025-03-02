import socket
from math import pow

def power(a, b, c):
    x = 1
    y = a
    while b > 0:
        if b % 2 == 0:
            x = (x * y) % c
        y = (y * y) % c
        b = int(b / 2)
    return x % c

def encrypt(msg, q, h, g):
    ct = []
    k = 3  # Let's use a fixed value for k in this example
    s = power(h, k, q)
    p = power(g, k, q)
    for i in range(0, len(msg)):
        ct.append(msg[i])
    for i in range(0, len(ct)):
        ct[i] = s * ord(ct[i])
    return ct, p

# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 12345

client_socket.connect((host, port))
print(f"Connected to server at {host}:{port}")

# Receive public parameters from server
data = client_socket.recv(1024).decode().split(',')
q, g, h = int(data[0]), int(data[1]), int(data[2])
print(f"Received public parameters from server:")
print(f"q (prime): {q}")
print(f"g (generator): {g}")
print(f"h (public key): {h}")

# Get message from user
msg = input("Enter the message to encrypt: ")

# Encrypt message
ct, p = encrypt(msg, q, h, g)
print(f"Original message: {msg}")
print(f"Encrypted message: {ct}")
print(f"Generated p: {p}")

# Send encrypted message to server
encrypted_msg = ','.join(map(str, ct)) + f',{p}'
client_socket.send(encrypted_msg.encode())

print("Encrypted message sent to server for decryption.")

client_socket.close()
