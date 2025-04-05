import socket
from rsa import populate_primes, generate_rsa_keys, show_keys, create_signature

filename = input("Enter file to transfer: ")
print(f"Selected File: {filename}")

client_sock = socket.socket()
client_sock.connect(('localhost', 9999))
print("Connected to server")

# Get server public key
server_keys = client_sock.recv(1024).decode().split()
server_e = int(server_keys[0])
server_n = int(server_keys[1])
print("\nServer Public Details:")
print(f"Public Key: {server_e}")
print(f"Modulus: {server_n}")

populate_primes()
generate_rsa_keys()
client_e, client_n = show_keys()

# Send client public key
client_sock.send(f"CLIENT_KEY|{client_e}|{client_n}".encode())
print("Sent client credentials to server")

# Read and sign file
with open(filename, "rb") as f:
    file_content = f.read()

print("\nSignature Generation:")
signature = create_signature(file_content)
print(f"Generated Signature: {signature}")

# Send file metadata
client_sock.send(f"FILE_INFO|{filename}|{signature}".encode())
print("Sent file metadata to server")

# Send file content
with open(filename, "rb") as f:
    while True:
        chunk = f.read(4096)
        if not chunk: break
        client_sock.send(chunk)
        print(f"Sent Data Chunk: {len(chunk)} bytes")

client_sock.close()
print("\nClient: Transfer completed")
