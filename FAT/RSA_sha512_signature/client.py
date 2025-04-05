import socket
import json
import hashlib

# RSA parameters
p = 61
q = 53
n = p * q
phi = (p-1) * (q-1)
e = 17  # Public exponent
d = pow(e, -1, phi)  # Private key

# Read message and compute hash
with open("message.txt", "r") as f:
    text = f.read().strip()

hash_bytes = hashlib.sha256(text.encode()).digest()
hash_int = int.from_bytes(hash_bytes, byteorder='big') % n

# Generate signature
signature = pow(hash_int, d, n)

# Connect to verification server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 3000))

# Prepare and send data
data = {
    "text": text,
    "signature": hex(signature),  # Send as hex string
    "public_key": {"e": e, "n": n}
}

client_socket.sendall(json.dumps(data).encode())
print("Signature sent to verification server")
client_socket.close()
