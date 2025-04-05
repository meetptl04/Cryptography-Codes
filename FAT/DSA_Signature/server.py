import socket
import json
import hashlib

# Set up server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 3000))
server_socket.listen(1)
print("Server ready to verify signatures...")

# Accept client connection
conn, addr = server_socket.accept()

# Receive and parse data
data = json.loads(conn.recv(4096).decode())
signature = data["signature"]
text = data["text"]
public_key = data["public_key"]

# Extract components
r = signature["r"]
s = signature["s"]
p = public_key["p"]
q = public_key["q"]
g = public_key["g"]
y = public_key["y"]

# Verification process
hash_hex = hashlib.sha256(text.encode()).hexdigest()
hash_int = int(hash_hex, 16) % q

try:
    w = pow(s, -1, q)
    u1 = (hash_int * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
except Exception as e:
    print(f"Verification error: {e}")
    exit()

print("Signature Verified" if v == r else "Verification Failed")
conn.close()
server_socket.close()
