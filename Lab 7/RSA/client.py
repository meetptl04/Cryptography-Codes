import socket
from RSA import encoder, decoder, fill_prime_numbers, set_keys

# Prepare to encode the message using the RSA algorithm
message = input("Enter the plaintext: ")
print(f"Initial message: {message}")

# Create a socket connection to the server
client_socket = socket.socket()
client_socket.connect(('localhost', 9999))

# Receive the public key (e, n) from the server
public_key_info = client_socket.recv(1024).decode()
num1, num2 = map(int, public_key_info.split())

# Print the public key
print(f"Received Public Key (e, n): {num1}, {num2}")

# Encrypt the message using the public key
encoded_message = encoder(message, num1, num2)

# Convert the encrypted message into a space-separated string
encoded_message_str = ' '.join(map(str, encoded_message))

print("\nThe encrypted message (sent to the server):")
print(encoded_message_str)

# Send the encrypted message to the server
client_socket.send(encoded_message_str.encode("utf-8"))

client_socket.close()
