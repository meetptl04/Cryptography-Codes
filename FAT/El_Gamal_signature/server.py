import socket
import hashlib
import json

server_socket = socket.socket()
server_socket.bind(("localhost", 1234))
server_socket.listen(1)
conn, addr = server_socket.accept()

# Receive public keys
public_key = json.loads(conn.recv(4096).decode())
alpha , Ya , p = public_key["alpha"] , public_key["Ya"] , public_key["p"]

# Receive message + signature
signature_data = json.loads(conn.recv(4096).decode())
text , s1 , s2 = signature_data["text"] , signature_data["s1"] , signature_data["s2"]

# Verification
hash_hex = hashlib.sha256(text.encode()).hexdigest()
hash_int = int(hash_hex, 16) % (p-1)

v1 = pow(alpha, hash_int, p)
v2 = (pow(Ya, s1, p) * pow(s1, s2, p)) % p

print("Signature Verified" if v1 == v2 else "Signature Invalid")
server_socket.close()