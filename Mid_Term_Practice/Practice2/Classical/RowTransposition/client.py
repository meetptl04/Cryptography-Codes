import socket

def row_transposition_encrypt(text, key):
    cols = len(key)
    rows = len(text) // cols
    if len(text) % cols != 0:
        rows += 1
    text += "X" * (rows * cols - len(text))
    matrix = [list(text[i * cols:(i + 1) * cols]) for i in range(rows)]
    order = sorted(list(enumerate(key)), key=lambda x: x[1])
    ciphertext = ""
    for index, _ in order:
        for row in matrix:
            ciphertext += row[index]
    return ciphertext

def client():
    s = socket.socket()
    s.connect(('localhost', 8080))
    key = input("Enter the Key : ")
    msg = input("Enter message: ")
    encrypted = row_transposition_encrypt(msg, key)
    print(f"Encrypted: {encrypted}")
    s.send(key.encode())
    s.send(encrypted.encode())
    s.close()

client()
