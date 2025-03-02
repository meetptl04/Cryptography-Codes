import socket
import numpy as np

# Define constants for block size and number of rounds in the encryption process
BLOCK_SIZE = 16
NUM_ROUNDS = 12

# Function to generate a substitution box (S-Box) for encryption and decryption
def generate_sbox():
    sbox = np.arange(256, dtype=np.uint8)  # Initialize an array of numbers from 0 to 255
    j = 0
    for i in range(256):
        j = (j + sbox[i]) % 256  # Update j using modular arithmetic
        sbox[i], sbox[j] = sbox[j], sbox[i]  # Swap the elements at indices i and j
    return sbox  # Return the generated S-Box

# Function to decrypt the ciphertext
def decrypt(ciphertext):
    # Check if the ciphertext length is a multiple of the block size, raise an error if not
    if len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Invalid ciphertext length")

    sbox = generate_sbox()  # Generate the S-Box used for decryption
    inverse_sbox = np.argsort(sbox)  # Generate the inverse of the S-Box

    decrypted = bytearray(ciphertext)  # Convert ciphertext into a bytearray

    # Iterate over the ciphertext in blocks of BLOCK_SIZE
    for offset in range(0, len(decrypted), BLOCK_SIZE):
        # Perform decryption for a defined number of rounds in reverse order
        for round_num in reversed(range(NUM_ROUNDS)):
            # Apply a simple reverse permutation (rotation) of the block
            temp = [0] * BLOCK_SIZE
            for i in range(BLOCK_SIZE):
                old_pos = (i - round_num) % BLOCK_SIZE  # Compute the original position after reverse rotation
                temp[old_pos] = decrypted[offset + i]
            for i in range(BLOCK_SIZE):
                decrypted[offset + i] = temp[i]  # Update the block with the rotated values

            # Apply the inverse S-Box substitution to each byte in the current block
            for i in range(BLOCK_SIZE):
                decrypted[offset + i] = inverse_sbox[decrypted[offset + i]]

    # Retrieve the padding length and return the decrypted message (removing the padding)
    padding_length = decrypted[-1]
    return bytes(decrypted[:-padding_length])  # Remove padding and return the decrypted data

# Client Setup
HOST = '127.0.0.1'  # Localhost IP address
PORT = 65432  # Port to connect to on the server

# Create a socket object for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))  # Connect to the server at the specified host and port

# User enters the message to be encrypted and sends it to the server
plaintext = input("Enter a message to encrypt: ").encode()  # Convert the plaintext to bytes
print(f"Sending plaintext: {plaintext.decode()}")  # Display the plaintext message being sent
client_socket.sendall(plaintext)  # Send the plaintext message to the server

# Receive the encrypted data from the server
encrypted_data = client_socket.recv(1024)
if encrypted_data:
    # Print the ciphertext in hexadecimal format for consistency
    encrypted_hex = encrypted_data.hex()
    print(f"Ciphertext in hex: {encrypted_hex}")

    # Decrypt the received ciphertext
    decrypted_data = decrypt(encrypted_data)  # Decrypt the ciphertext using the decrypt function
    print(f"Decrypted message: {decrypted_data.decode()}")  # Display the decrypted message

# Close the connection once done
client_socket.close()
