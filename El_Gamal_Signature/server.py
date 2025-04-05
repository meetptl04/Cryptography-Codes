import socket
from ElGamal import verify

server_socket = socket.socket()
server_socket.bind(("localhost", 9999))
server_socket.listen(1)
print("Server listening...")

client_socket, addr = server_socket.accept()
print(f"Connected: {addr}")

# Receive client's public key
client_key_info = client_socket.recv(1024).decode().strip()
print(f"Received from client: {client_key_info}")
p, g, h = map(int, client_key_info.split("|")[1:])
public_key = (p, g, h)
print(f"Client public key:\nP: {p}\nG: {g}\nH: {h}")

# Receive file info
file_info = client_socket.recv(1024).decode().strip()
print(f"Received from client: {file_info}")
_, filename, r, s = file_info.split("|")
signature = (int(r), int(s))
print(f"File info received:\nFilename: {filename}\nSignature: {signature}")

# Receive file data
file_data = b""
while True:
    chunk = client_socket.recv(4096)
    if not chunk:
        break
    file_data += chunk
    print(f"Received file chunk of size {len(chunk)} bytes")
print(f"Total file size received: {len(file_data)} bytes")

# Verify signature
valid = verify(file_data, signature, public_key)
print(f"\nVerification {'SUCCEEDED' if valid else 'FAILED'}!")

client_socket.close()
server_socket.close()
