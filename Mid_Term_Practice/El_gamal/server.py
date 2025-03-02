import socket
import random
# from math import pow

# El_Gamal Key generation
def gen_key(q):
    key = random.randint(pow(10,20),q)
    while gcd(q, key) != 1:
        key = random.randint(pow(10, 20), q)
    return key

# GCD
def gcd(a,b):
    if a < b:
        return gcd(b,a)
    elif a % b == 0:
        return b
    else:
        return gcd(b,a % b)


# modulo
def power(a,b,c):
    return pow(a,b,c)

# def power(a, b, c):
#     x = 1
#     y = a
#     while b > 0:
#         if b % 2 == 0:
#             x = (x * y) % c
#         y = (y * y) % c
#         b = int(b / 2)
#     return x % c

# Decryption

def decryption(C2,C1,key,q):
    pt = []
    x = power(C1,key,q)
    for i in range(0,len(C2)):
        # pt.append(chr(C2[i]*power(x,q-2,q)))
        pt.append(chr(int(C2[i] / x)))
    return ''.join(pt)


server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(('localhost',12345))
server_socket.listen(1)

print(f"Server is waiting for connection...")

# Generate EL_Gamal parameters

q = random.randint(pow(10,20),pow(10,50))
g = random.randint(2,q)
key = gen_key(q)
h = power(g,key,q)

print(f"Generated El_Gamal Parameters : ")
print(f"g (prime) : {q}")
print(f"g (generator : primitive root) : {g}")
print(f"Private key : {key}")
print(f"Public key : {h}")

while True:
    conn , addr = server_socket.accept()
    print(f"Connected By {addr}")

    # Send public parameters to client
    conn.send(f"{q},{g},{h}".encode())
    print(f"Send public parameters to client : q = {q} , g = {g} , h = {h}")

    data = conn.recv(1024).decode().split(',')

    C2 = [int(x) for x in data[:-1]]
    C1 = int(data[-1])

    print(f"Received Encrypted Message : {C2}")
    print(f"Received C1 : {C1}")

    # Decryption
    decrypted_msg = decryption(C2,C1,key,q)

    print(f"Decrypted Message is  : {decrypted_msg}")

    conn.close()
    break


