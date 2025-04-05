import socket
from rsa import populate_primes, generate_rsa_keys, show_keys, verify_signature

populate_primes()
generate_rsa_keys()
server_e, server_n = show_keys()

serv_sock = socket.socket()
serv_sock.bind(("localhost", 9999))
serv_sock.listen(1)
print("\nServer Status: Waiting for connection...")

conn, addr = serv_sock.accept()
print(f"Connected to: {addr}")

# Send server public key
conn.send(f"{server_e} {server_n}".encode())
print("Sent server public key to client")

# Receive client public key
client_keys = conn.recv(1024).decode().split("|")
client_e = int(client_keys[1])
client_n = int(client_keys[2])
print("\nClient Public Details:")
print(f"Public Key: {client_e}")
print(f"Modulus: {client_n}")

# Receive file metadata
file_info = conn.recv(1024).decode().split("|")
fname = file_info[1]
sig = int(file_info[2])
print(f"\nIncoming File: {fname}")
print(f"File Signature: {sig}")

# Receive file content
with open(fname, "wb") as f:
    while True:
        data = conn.recv(4096)
        if not data: break
        print(f"Received Data Chunk: {len(data)} bytes")
        f.write(data)

# Verify signature
with open(fname, "rb") as f:
    content = f.read()

print("\nVerification Process:")
if verify_signature(sig, content, client_e, client_n):
    print("Signature Validation: Successful")
else:
    print("Signature Validation: Failed")

conn.close()
serv_sock.close()
print("\nServer: Transfer completed")
