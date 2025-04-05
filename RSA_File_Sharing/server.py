import socket
from RSA import fill_prime_numbers, set_keys, get_keys, verify

# Initialize the server's RSA keys.
fill_prime_numbers()
set_keys()
public_key, n = get_keys()
print(f"Server's Public Key (e): {public_key}")
print(f"Server's n: {n}")

# Set up the server socket.
server_socket = socket.socket()
server_socket.bind(("localhost", 9999))
server_socket.listen(1)
print("Server is listening...")

# Accept a connection from the client.
client_socket, addr = server_socket.accept()
print(f"Connected with {addr}")

# Send the server's public key info to the client.
public_key_info = f"{public_key} {n}"
print(f"Sending to client: {public_key_info}")
client_socket.send(public_key_info.encode("utf-8"))

# Receive client's public key FIRST
client_key_info = client_socket.recv(1024).decode()
print("Received client key info:", client_key_info)
parts = client_key_info.split("|")
if len(parts) != 3 or parts[0] != "CLIENT_KEY":
    print("Invalid client key format!")
    client_socket.close()
    server_socket.close()
    exit()

client_pub_key = int(parts[1])
client_n = int(parts[2])
print(f"Client's Public Key (e): {client_pub_key}")
print(f"Client's n: {client_n}")

# Receive file info SECOND
file_info = client_socket.recv(1024).decode()
print("Received file info:", file_info)
parts = file_info.split("|")
if len(parts) != 3 or parts[0] != "FILE_INFO":
    print("Invalid file info format!")
    client_socket.close()
    server_socket.close()
    exit()

file_name = parts[1]
signature = int(parts[2])
print(f"File name: {file_name}")
print(f"Signature: {signature}")

# Receive the file content and write it to disk.
with open(file_name, "wb") as file:
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        print(f"Received file chunk: {len(data)} bytes")
        file.write(data)

# Verify the signature
with open(file_name, "rb") as file:
    file_data = file.read()
print(f"File data read for verification: {len(file_data)} bytes")

if verify(signature, file_data, client_pub_key, client_n):
    print("File signature verified successfully.")
else:
    print("File signature verification failed.")

client_socket.close()
server_socket.close()
print("File received and connection closed.")
