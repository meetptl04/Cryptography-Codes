import socket

def vigenere_encrypt(text, key):
    text = text.upper()
    key = key.upper()
    result = ""
    key_length = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i % key_length]) - ord('A')
            result += chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
        else:
            result += char
    return result

def client():
    s = socket.socket()
    s.connect(('localhost', 8080))
    key = input("Enter the Key : ")
    msg = input("Enter message: ")
    encrypted = vigenere_encrypt(msg, key)
    print(f"Encrypted: {encrypted}")
    s.send(key.encode())
    s.send(encrypted.encode())
    s.close()

client()
