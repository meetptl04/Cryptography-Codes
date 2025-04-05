import socket
from ElGamal import generate_keys, sign

filename = input("Enter file to send: ")
print(f"Sending: {filename}")

client_socket = socket.socket()
client_socket.connect(("localhost", 9999))

# Generate and send keys
public_key, private_key = generate_keys(16)
p, g, h = public_key
client_key_info = f"CLIENT_KEY|{p}|{g}|{h}"
print(f"Sending to server: {client_key_info}")
client_socket.send(client_key_info.encode())

# Sign file
with open(filename, "rb") as f:
    file_data = f.read()
r, s = sign(file_data, private_key, p, g)
file_info = f"FILE_INFO|{filename}|{r}|{s}"
print(f"Sending to server: {file_info}")
client_socket.send(file_info.encode())

# Send file data in chunks
with open(filename, "rb") as f:
    while chunk := f.read(4096):
        print(f"Sending file chunk of size {len(chunk)} bytes")
        client_socket.send(chunk)

print("File sent successfully.")
client_socket.close()
