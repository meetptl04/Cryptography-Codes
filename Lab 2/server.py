import socket
from sdes import SimplifiedDES

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))
server_socket.listen(1)
print("Server is listening on port 65432")

# Accept connection
conn, addr = server_socket.accept()
print(f"Connection from {addr}")

# Receive client's key choice
key_choice = conn.recv(1024).decode().strip().lower()

# Set key based on the client's choice
if key_choice == "no":
    # If the client wants a custom key, server will wait for it
    custom_key = conn.recv(1024).decode().strip()
    key = [int(bit) for bit in custom_key]
    print(f"Server using custom key from client: {key}")
else:
    key = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]  # Default key
    print(f"Server using default key: {key}")

# Initialize SDES with the chosen key
sdes = SimplifiedDES(key)
sdes.key_generation()

while True:
    data = conn.recv(1024).decode()
    if data.lower() == "exit":
        print("Client has exited the chat.")
        break

    print(f"Received encrypted text from client: {data}")
    ciphertext = [int(b) for b in data]
    decrypted_message = ''.join(map(str, sdes.decrypt(ciphertext)))
    print(f"Decrypted text: {decrypted_message}")

    server_message = input("You (plaintext): ")
    if server_message.lower() == "exit":
        conn.send("exit".encode())
        print("Exiting the chat.")
        break

    plaintext = [int(b) for b in server_message]
    encrypted_response = sdes.encrypt(plaintext)
    encrypted_response_str = ''.join(map(str, encrypted_response))
    print(f"Encrypted text to send to client: {encrypted_response_str}")
    conn.send(encrypted_response_str.encode())

conn.close()
