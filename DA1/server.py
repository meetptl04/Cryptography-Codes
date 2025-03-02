import socket
import numpy as np

# Define constants for block size and number of rounds in the encryption process
BLOCK_SIZE = 16
NUM_ROUNDS = 12

# Function to generate a substitution box (S-Box) for encryption
def generate_sbox():
    sbox = np.arange(256, dtype=np.uint8)  # Initialize an array of numbers from 0 to 255
    j = 0
    for i in range(256):
        j = (j + sbox[i]) % 256  # Update j using modular arithmetic
        sbox[i], sbox[j] = sbox[j], sbox[i]  # Swap the elements at indices i and j
    return sbox  # Return the generated S-Box

# Function to encrypt the plaintext
def encrypt(plaintext):
    # Calculate the padding length needed to make the plaintext a multiple of BLOCK_SIZE
    padding_length = BLOCK_SIZE - (len(plaintext) % BLOCK_SIZE)
    padded_length = len(plaintext) + padding_length
    padded = bytearray(plaintext)  # Convert plaintext into bytearray
    padded.extend([padding_length] * padding_length)  # Add padding bytes at the end

    sbox = generate_sbox()  # Generate the S-Box

    # Iterate over the padded plaintext in blocks of BLOCK_SIZE
    for offset in range(0, len(padded), BLOCK_SIZE):
        # Perform encryption for a defined number of rounds
        for round_num in range(NUM_ROUNDS):
            # Apply S-Box substitution to each byte in the current block
            for i in range(BLOCK_SIZE):
                padded[offset + i] = sbox[padded[offset + i]]

            # Perform a simple permutation (rotation) of the block
            temp = [0] * BLOCK_SIZE
            for i in range(BLOCK_SIZE):
                new_pos = (i + round_num) % BLOCK_SIZE  # Compute the new position for rotation
                temp[new_pos] = padded[offset + i]
            for i in range(BLOCK_SIZE):
                padded[offset + i] = temp[i]  # Update the block with the rotated values

    return bytes(padded)  # Return the encrypted data as bytes

# Server Setup
HOST = '127.0.0.1'  # Localhost IP address
PORT = 65432  # Port for communication

# Create a socket object for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))  # Bind the socket to the specified address and port
server_socket.listen(1)  # Enable the server to accept 1 connection at a time

print("Server is running and waiting for a connection...")

# Accept an incoming connection from a client
conn, addr = server_socket.accept()
print(f"Connected by {addr}")  # Print the address of the connected client

# Receive data from the client
data = conn.recv(1024)
if data:
    print(f"Received plaintext: {data.decode()}")  # Display the received plaintext
    encrypted_data = encrypt(data)  # Encrypt the received plaintext
    print(f"Encrypted data: {encrypted_data.hex()}")  # Display the encrypted data in hexadecimal format

    # Send the encrypted data back to the client
    conn.sendall(encrypted_data)

# Close the connection and the server socket
conn.close()
server_socket.close()
