import socket
import hashlib
import json
import random
from math import gcd

client_socket = socket.socket()
client_socket.connect(("localhost", 1234))

# Public key parameters
p = 11
alpha = 10  # Primitive root modulo 11
Xa = 3      # Valid private key (1 < Xa < 10)
Ya = pow(alpha, Xa, p)

# Send public keys
public_key = {"alpha": alpha, "Ya": Ya, "p": p}
client_socket.sendall(json.dumps(public_key).encode())

# Read message
with open("message.txt", "r") as f:
    text = f.read()

# Generate valid r (coprime with p-1)
while True:
    r = random.randint(2, p-2)  # 1 < r < p-1
    if gcd(r, p-1) == 1:
        break

try:
    r_inv = pow(r, -1, p-1)  # Now safe (r and p-1 are coprime)
except ValueError:
    print(f"Error: No inverse for r={r} mod {p-1}")
    exit()

# Compute hash and signature
hash_hex = hashlib.sha256(text.encode()).hexdigest()
hash_int = int(hash_hex, 16) % (p-1)

s1 = pow(alpha, r, p)
s2 = ((hash_int - (Xa * s1) % (p-1)) * r_inv) % (p-1)

# Send message + signature
signature_pair = {"text": text, "s1": s1, "s2": s2}
client_socket.sendall(json.dumps(signature_pair).encode())
client_socket.close()
