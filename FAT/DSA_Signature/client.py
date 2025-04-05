import socket
import json
import hashlib
import random
from math import gcd

# DSA parameters
p = 1019
q = 509  # Prime divisor of p-1
h = 2
g = pow(h, (p-1)//q, p)

# Generate keys
x = random.randint(1, q-1)  # Private key
y = pow(g, x, p)            # Public key

# Read message
with open("message.txt", "r") as f:
    text = f.read().strip()

# Generate signature
hash_hex = hashlib.sha256(text.encode()).hexdigest()
hash_int = int(hash_hex, 16) % q

while True:
    k = random.randint(1, q-1)
    if gcd(k, q) == 1:  # Ensure k is invertible
        break

k_inv = pow(k, -1, q)
r = pow(g, k, p) % q
s = (k_inv * (hash_int + x * r)) % q

# Prepare and send data
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 3000))

data = {
    "text": text,
    "signature": {"r": r, "s": s},
    "public_key": {"p": p, "q": q, "g": g, "y": y}
}

client_socket.sendall(json.dumps(data).encode())
print("Signature sent for verification")
client_socket.close()
