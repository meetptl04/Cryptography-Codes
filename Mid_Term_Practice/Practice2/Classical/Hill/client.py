import socket
import numpy as np

def text_to_numbers(text):
    return [ord(char) - ord('A') for char in text]

def encrypt(msg, key_matrix):
    msg_nums = text_to_numbers(msg)
    msg_nums += [0] * ((3 - len(msg_nums) % 3) % 3)  # Padding if needed
    msg_matrix = np.array(msg_nums).reshape(-1, 3)
    # Multiply by the transpose of key matrix
    cipher_nums = (np.dot(msg_matrix, key_matrix.T) % 26).flatten()
    return ''.join(chr(num + ord('A')) for num in cipher_nums)

def get_key_matrix():
    while True:
        key = input("Enter 9-letter key (A-Z): ").upper()
        if len(key) == 9 and key.isalpha():
            return np.array([ord(c) - ord('A') for c in key]).reshape(3, 3)
        print("Invalid key! Enter exactly 9 uppercase letters.")

def client():
    s = socket.socket()
    s.connect(('localhost', 8080))

    key_matrix = get_key_matrix()
    msg = input("Enter message (UPPERCASE, length multiple of 3): ").upper()

    encrypted_msg = encrypt(msg, key_matrix)
    print(f"Encrypted: {encrypted_msg}")

    s.send(str(key_matrix.tolist()).encode())
    s.send(encrypted_msg.encode())
    s.close()

client()
