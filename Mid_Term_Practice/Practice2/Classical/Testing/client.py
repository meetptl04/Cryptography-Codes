import socket
from helper import playfair_encrypt,playfair_decrypt

def vignere_encrypt(msg,key):
    encrypted = ""
    key = key.upper()
    msg = msg.upper()
    key_length = len(key)
    for i,char in enumerate(msg):
        if char.isalpha():
            shift = ord(key[i%key_length]) - ord('A')
            encrypted += chr((ord(char) - ord('A') + shift)%26 + ord('A'))
        else:
            encrypted += char
    return encrypted

def raw_transposition_encrypt(msg,key):
    encrypted = ""
    cols = len(key)
    rows = len(msg)//cols
    if len(msg)%cols != 0:
        rows += 1
    msg += "X"*(rows*cols - len(msg))
    matrix = [list(msg[i*cols:(i+1)*cols]) for i in range(rows)]
    order = sorted(list(enumerate(key)) ,key=lambda x:x[1])
    for index , _ in order:
        for row in matrix:
            encrypted += row[index]
    return encrypted

def rail_fence_encrypt(msg,rails):
    if rails <= 1: return msg
    fence,rail , direction = ['']*rails,0,1
    for char in msg:
        fence[rail] += char
        rail += direction
        if rail == rails - 1 or rail == 0:
            direction = -direction
    return ''.join(fence)

def client():
    s = socket.socket()
    s.connect(('localhost',8080))
    key = input("Enter the key:")
    msg = input("Enter the message:")
    # encrypted = vignere_encrypt(msg,key)
    # encrypted = raw_transposition_encrypt(msg,key)

    # rail fence
    # key = int(key)
    # encrypted = rail_fence_encrypt(msg,key)
    # s.send(str(key).encode())

    # Play Fair
    encrypted = playfair_encrypt(msg,key)

    s.send(key.encode())
    s.send(encrypted.encode())
    s.close()

client()
