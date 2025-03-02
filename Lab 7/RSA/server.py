import socket
from RSA import encoder, decoder, fill_prime_numbers, set_keys, get_keys

# Initialize RSA keys
fill_prime_numbers()
set_keys()
public_key, n = get_keys()

# At this point, private key is already generated
# So now we print public and private keys after generation
print("Public Key (e, n):", public_key, n)

# Set up the server
server_socket = socket.socket()
server_socket.bind(("localhost", 9999))
server_socket.listen(1)

print("Server is listening...")

# Accept a connection from a client
client_socket, addr = server_socket.accept()
print(f"Connected with {addr}")

# Send public key to the client
public_key_info = f"{public_key} {n}"
client_socket.send(public_key_info.encode("utf-8"))

# Receive the encrypted message from the client
cipher_text = client_socket.recv(2048)
print(f"Received encrypted message: {cipher_text.decode()}")

# Decode the received cipher text into a list of integers
encoded_message = list(map(int, cipher_text.decode().split()))

# Decrypt the message using the private key
decrypted_text = decoder(encoded_message)

# Now we print the private key only after the decryption process
# print("Private Key (d):", private_key)
print("Decrypted message (using private key):")
print(decrypted_text)

client_socket.close()
server_socket.close()
