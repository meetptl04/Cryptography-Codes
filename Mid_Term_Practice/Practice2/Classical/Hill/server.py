import socket
import numpy as np

def mod_inverse_matrix(matrix, mod=26):
    try:
        det = int(round(np.linalg.det(matrix)))  # Compute determinant
        det_inv = pow(det, -1, mod)              # Modular inverse of determinant
        adjugate = np.round(np.linalg.inv(matrix) * det).astype(int)
        return (det_inv * adjugate % mod).astype(int)
    except ValueError:  # Raised if modular inverse doesn't exist
        print("Inverse is not possible")
        return None

def decrypt(cipher_text, key_matrix):
    key_inv = mod_inverse_matrix(key_matrix)
    if key_inv is None:
        return ""
    # Convert ciphertext letters to numbers (A=0,...,Z=25)
    cipher_nums = [ord(char) - ord('A') for char in cipher_text]
    cipher_matrix = np.array(cipher_nums).reshape(-1, 3)
    decrypted_nums = (np.dot(cipher_matrix, key_inv.T) % 26).astype(int)
    return ''.join(chr(num + ord('A')) for num in decrypted_nums.flatten())

def server():
    s = socket.socket()
    s.bind(('localhost', 8080))
    s.listen(1)
    conn, _ = s.accept()

    key_matrix = np.array(eval(conn.recv(1024).decode()))
    cipher_text = conn.recv(1024).decode()

    print(f"Encrypted: {cipher_text}")
    decrypted_msg = decrypt(cipher_text, key_matrix)
    if decrypted_msg:
        print(f"Decrypted: {decrypted_msg}")
    conn.close()
    s.close()

server()
