import socket
import json
import hashlib

# Set up verification server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 3000))
server_socket.listen(1)
print("Verification server ready...")

conn, addr = server_socket.accept()
print(f"Connection from {addr}")

# Receive data from client
data = json.loads(conn.recv(4096).decode())

# Extract components
text = data["text"]
signature = int(data["signature"], 16)  # Convert hex to integer
public_key = data["public_key"]

# Verification process
e = public_key["e"]
n = public_key["n"]

computed_hash = hashlib.sha256(text.encode()).hexdigest()
computed_hash_int = int(computed_hash, 16) % n

decrypted_hash = pow(signature, e, n)

if decrypted_hash == computed_hash_int:
    print("RSA Signature Verified")
else:
    print("Verification Failed")

conn.close()
server_socket.close()
