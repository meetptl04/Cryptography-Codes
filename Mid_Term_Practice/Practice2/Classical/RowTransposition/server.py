import socket

def row_transposition_decrypt(cipher, key):
    cols = len(key)
    rows = len(cipher) // cols
    order = sorted(list(enumerate(key)), key=lambda x: x[1])
    matrix = [[''] * cols for _ in range(rows)]
    index = 0
    for col_index, _ in order:
        for r in range(rows):
            matrix[r][col_index] = cipher[index]
            index += 1
    plaintext = ''.join(''.join(row) for row in matrix)
    return plaintext.rstrip("X")

def server():
    s = socket.socket()
    s.bind(('localhost', 8080))
    s.listen(1)
    c, _ = s.accept()
    key = c.recv(1024).decode()
    encrypted = c.recv(1024).decode()
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {row_transposition_decrypt(encrypted, key)}")
    c.close()
    s.close()

server()
