import socket
# from math import pow

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

# Encryption
def encrypt(msg,q,h,g):
    C2 = []
    k = 3
    C1 = power(g,k,q)
    temp = power(h,k,q)
    for i in range(0,len(msg)):
        C2.append(msg[i])
    for i in range(0,len(msg)):
        C2[i] = temp * ord(C2[i])

    return C2,C1



client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(('localhost',12345))

print(f"Connected to server")

data = client_socket.recv(1024).decode().split(',')
q , g , h = int(data[0]) , int(data[1]) , int(data[2])
print(f"Received public parameters from server:")
print(f"q (prime): {q}")
print(f"g (generator): {g}")
print(f"h (public key): {h}")

# Input a message

msg = input("Enter the message to encrypt : ")

# Encryption part
# here (C2,C1) Here  C2 = msg * h^k mod q and C1 = g^k mod q

C2 , C1 = encrypt(msg,q,h,g)

print(f"Original Message : {msg}")
print(f"Encrypted Message : {C2}")
print(f"Generator : {C1}")

encrypted_msg = ','.join(map(str,C2)) + f',{C1}'
client_socket.send(encrypted_msg.encode())

print(f"Encrypted Message send to server for decryption")

client_socket.close()

