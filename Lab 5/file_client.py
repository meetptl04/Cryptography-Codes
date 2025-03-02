import socket
from des import des_encrypt
from tkinter import filedialog, Tk
import time
import sys

start = time.time()
# Function to convert normal binary data to hexadecimal representation
def bytes_to_hex(byte_data):
    return byte_data.hex()


# Function to split hex data into 16-character blocks (64-bit DES blocks)
def split_into_blocks(hex_data, block_size=16):
    """Splits hex data into fixed-size blocks, padding the last block if necessary."""
    blocks = [hex_data[i:i + block_size] for i in range(0, len(hex_data), block_size)]

    # Pad last block if it's smaller than BLOCK_SIZE (16 hex chars = 8 bytes)
    if len(blocks[-1]) < block_size:
        blocks[-1] = blocks[-1].ljust(block_size, '0')  # Padding with '0'

    return blocks


# Function to encrypt file in ECB mode
def encrypt_ecb_file(file_path, key):
    encrypted_blocks = []

    with open(file_path, "rb") as file:
        file_data = file.read()  # Read entire file as bytes

    hex_data = bytes_to_hex(file_data)  # Convert to hex
    blocks = split_into_blocks(hex_data)  # Split into blocks
    i = 0
    for block in blocks:
        start_time = time.time() # Record the start time
        encrypted_blocks.append(des_encrypt(str(block), key))  # Encrypt each block
        end_time = time.time()  # Record the end time
        time_taken = end_time - start_time  # Calculate the time difference
        print(f"Time taken to encrypt the block {i} : {time_taken:.10f} seconds")
        i += 1
    print(f"Total Time to encrypt the file : {time.time()-start}")
    return encrypted_blocks


# Set up Tkinter file dialog
root = Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title="Select a file to encrypt")

if not file_path:
    print("No file selected, exiting.")
    exit()

# key = "AABB09182736CCDD"
key = "aabb09182736ccdd"
c = socket.socket()
c.connect(('localhost', 8080))  # Connect to server

# Encrypt the file in ECB mode
encrypted_blocks = encrypt_ecb_file(file_path, key)

# Send encrypted blocks
for encrypted_block in encrypted_blocks:
    c.send(encrypted_block.encode())  # Ensure bytes format for transmission

# c.send(b"EOF")  # End of File signal
c.send("EOF".encode())  # Send "EOF" as bytes

print("Encrypted Data : ")
for encrypted_block in encrypted_blocks:
    print(f"{encrypted_block}")

# Save encrypted file as normal text
with open("encrypted_file.txt", "w") as file:
    for encrypted_block in encrypted_blocks:
        file.write(encrypted_block)

# Receive decrypted file
with open("downloaded_decrypted_file.txt", "wb") as download_file:
    while chunk := c.recv(1024):
        if chunk == b"EOF":
            break
        download_file.write(chunk)

print("Decrypted file downloaded from server.")
c.close()

sys.exit()


