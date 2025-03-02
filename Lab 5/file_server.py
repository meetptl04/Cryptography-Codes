import socket
from des import des_decrypt
import time
import sys

start = time.time()
# Function to convert hex string data to bytes
def hex_to_bytes(hex_data):
    return bytes.fromhex(hex_data)

# Function to convert decrypted hex data back to normal text
def hex_to_normal_text(hex_data):
    # Convert hex string to bytes
    byte_data = hex_to_bytes(hex_data)

    # Attempt to decode byte data to normal text (assumes UTF-8 encoded text)
    try:
        return byte_data.decode('utf-8')
    except UnicodeDecodeError:
        print("Error decoding byte data. The content may not be in UTF-8 format.")
        return byte_data  # Return raw byte data if decoding fails

# Function to decrypt file in ECB mode
def decrypt_ecb_file(encrypted_blocks, key):
    decrypted_data = ""
    i = 0
    for encrypted_block in encrypted_blocks:
        start_time = time.time()  # Record the start time
        decrypted_data += des_decrypt(encrypted_block, key)
        end_time = time.time()  # Record the end time
        time_taken = end_time - start_time  # Calculate the time difference
        print(f"Time taken to decrypt the block {i} : {time_taken:.10f} seconds")
        i += 1
    print(f"Total Time to decrypt the file : {time.time()-start}")
    return decrypted_data

# Set up server to accept client connections
s = socket.socket()
s.bind(("localhost", 8080))  # Listen on port 8080
s.listen(1)

print("Server is listening on port 8080")

# key = "AABB09182736CCDD"  # Shared key for encryption and decryption
key = "aabb09182736ccdd"

while True:
    c, addr = s.accept()
    print(f"Connected with {addr}")

    encrypted_blocks = []

    while True:
        encrypted_block = c.recv(16)  # Receive exactly 8 bytes per block
        if encrypted_block == b"EOF":  # End of File signal
            break
        encrypted_block = encrypted_block.decode('utf-8')
        encrypted_blocks.append(encrypted_block)

    # Decrypt the file
    decrypted_data = decrypt_ecb_file(encrypted_blocks, key)

    # Convert decrypted hex data to normal text
    decrypted_text = hex_to_normal_text(decrypted_data)

    # Save decrypted file as normal text
    with open("decrypted_received_file.txt", "w") as file:
        file.write(decrypted_text)

    print("Decrypted file saved as 'decrypted_received_file.txt'.")

    # Send decrypted file back
    with open("decrypted_received_file.txt", "rb") as file:
        while chunk := file.read(1024):
            c.send(chunk)

    c.close()
    print("Connection closed.")

    sys.exit()


