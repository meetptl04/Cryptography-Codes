import socket
from helper import playfair_encrypt,playfair_decrypt

def vigenere_decrypt(encrypted,key):
    decrypted = ""
    key = key.upper()
    encrypted = encrypted.upper()
    key_length = len(key)
    for i,char in enumerate(encrypted):
        if char.isalpha():
            shift = ord(key[i%key_length]) - ord('A')
            decrypted += chr((ord(char)-ord('A') - shift)%26 + ord('A'))
        else:
            encrypted += char
    return decrypted

def raw_transposition_decrypt(encrypted,key):
    cols = len(key)
    rows = len(encrypted)//cols
    order = sorted(list(enumerate(key)) , key = lambda x:x[1])
    matrix = [['']*cols for _ in range(rows)]
    index = 0
    for col_index , _ in order:
        for row_index in range(rows):
            matrix[row_index][col_index] = encrypted[index]
            index += 1
    plaintext = ''.join(''.join(row) for row in matrix)
    return plaintext.rstrip("X")

def rail_fence_decrypt(encrypted,rails):
    if rails <= 1 : return encrypted
    pattern , rail , direction = [] , 0 ,1
    for _ in encrypted:
        pattern.append(rail)
        rail += direction
        if rail == rails - 1 or rail == 0:
            direction = -direction

    rail_counts = [pattern.count(i) for i in range(rails)]
    rails_text, index = [], 0
    for count in rail_counts:
        rails_text.append(list(encrypted[index:index + count]))
        index += count
    return ''.join(rails_text[i].pop(0) for i in pattern)

def server():
    s = socket.socket()
    s.bind(('localhost',8080))
    s.listen(1)
    c , _ = s.accept()
    key = c.recv(1024).decode()
    # key = int(c.recv(1024).decode())
    encrypted = c.recv(1024).decode()
    # print(f"Enrypted message: {encrypted}")
    # print(f"Decrpted message : {vigenere_decrypt(encrypted,key)}")
    # print(f"Enrypted message: {encrypted}")
    # print(f"Decrpted message : {raw_transposition_decrypt(encrypted,key)}")

    # rail fence
    # print(f"Enrypted message: {encrypted}")
    # print(f"Decrpted message : {rail_fence_decrypt(encrypted,key)}")

    # Play Fair
    print(f"Enrypted message: {encrypted}")
    print(f"Decrpted message : {playfair_decrypt(encrypted,key)}")
    c.close()

server()
