import socket
import random
from math import pow

# ElGamal functions
def generate_keys(q):
    key = random.randint(pow(10, 20), q)
    while gcd(q, key) != 1:
        key = random.randint(pow(10, 20), q)
    return key

def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)

def power(a, b, c):
    x = 1
    y = a
    while b > 0:
        if b % 2 == 0:
            x = (x * y) % c
        y = (y * y) % c
        b = int(b / 2)
    return x % c

def decrypt(ct, p, key, q):
    pt = []
    h = power(p, key, q)
    for i in range(0, len(ct)):
        pt.append(chr(int(ct[i] / h)))
    return ''.join(pt)

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 12345
server_socket.bind((host, port))
server_socket.listen(1)

print("Server is waiting for connections...")

# Generate ElGamal parameters
q = random.randint(pow(10, 20), pow(10, 50))
g = random.randint(2, q)
key = generate_keys(q)
h = power(g, key, q)

print(f"Generated ElGamal parameters:")
print(f"q (prime): {q}")
print(f"g (generator): {g}")
print(f"Private key: {key}")
print(f"Public key (h): {h}")

while True:
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    # Send public parameters to client
    conn.send(f"{q},{g},{h}".encode())
    print(f"Sent public parameters to client: q={q}, g={g}, h={h}")

    # Receive encrypted message from client
    data = conn.recv(1024).decode().split(',')
    ct = [int(x) for x in data[:-1]]
    p = int(data[-1])

    print(f"Received encrypted message: {ct}")
    print(f"Received p: {p}")

    # Decrypt message
    decrypted_msg = decrypt(ct, p, key, q)
    print(f"Decrypted message: {decrypted_msg}")

    conn.close()
