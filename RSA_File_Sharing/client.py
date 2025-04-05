import socket
from RSA import fill_prime_numbers, set_keys, sign

# Ask the user for the file name to send.
file_name = input("Enter the file name to send: ")
print(f"File to send: {file_name}")

# Create a socket connection to the server.
client_socket = socket.socket()
client_socket.connect(('localhost', 9999))
print("Client connected to server.")

# Receive the server's public key info.
public_key_info = client_socket.recv(1024).decode()
print(f"Received from server: {public_key_info}")
num1, num2 = map(int, public_key_info.split())
print(f"Server's Public Key (e, n): {num1}, {num2}")

# Generate the client's RSA keys for signing.
fill_prime_numbers()
set_keys()
client_public_key = __import__('RSA').public_key
client_private_key = __import__('RSA').private_key
client_n = __import__('RSA').n
print(f"Client's Private Key (d): {client_private_key}")
print(f"Client's Public Key (e): {client_public_key}")
print(f"Client's n: {client_n}")

# Send client's public key (e, n) FIRST
client_key_info = f"CLIENT_KEY|{client_public_key}|{client_n}"
print("Sending client's public key to server:", client_key_info)
client_socket.send(client_key_info.encode("utf-8"))

# Read the file in binary mode.
with open(file_name, "rb") as file:
    file_data = file.read()
print(f"File data read: {len(file_data)} bytes")

# Sign the file data using the client's private key.
signature = sign(file_data)
print(f"File signature: {signature}")

# Send file info (file name and signature) SECOND
file_info = f"FILE_INFO|{file_name}|{signature}"
print(f"Sending file info to server: {file_info}")
client_socket.send(file_info.encode("utf-8"))

# Now send the file content in chunks.
with open(file_name, "rb") as file:
    while True:
        data = file.read(4096)
        if not data:
            break
        print(f"Sending file chunk: {len(data)} bytes")
        client_socket.send(data)

print("File sent to server.")
client_socket.close()
