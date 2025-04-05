import socket

def vigenere_decrypt(cipher, key):
    cipher = cipher.upper()
    key = key.upper()
    result = ""
    key_length = len(key)
    for i, char in enumerate(cipher):
        if char.isalpha():
            shift = ord(key[i % key_length]) - ord('A')
            result += chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
        else:
            result += char
    return result

def server():
    s = socket.socket()
    s.bind(('localhost', 8080))
    s.listen(1)
    c, _ = s.accept()
    key = c.recv(1024).decode()
    encrypted = c.recv(1024).decode()
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {vigenere_decrypt(encrypted, key)}")
    c.close()
    s.close()

server()
