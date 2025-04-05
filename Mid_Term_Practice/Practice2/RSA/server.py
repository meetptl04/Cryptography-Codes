import socket
import random
import json

def power(a, b, c):
    return pow(a, b, c)

def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)

def key_generate(phin):
    e = random.randint(2, phin - 1)
    while gcd(phin, e) != 1:
        e = random.randint(2, phin - 1)
    return e

def decrypt(encrypted, d, n):
    msg = ""
    for i in range(len(encrypted)):
        m = power(encrypted[i], d, n)
        msg += chr(m)
    return msg

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def generate_prime(lower, upper):
    while True:
        num = random.randint(lower, upper)
        if is_prime(num):
            return num

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)
    print(f"Yeah , I am Client : Hahahaha")
    # p = generate_prime(pow(10, 3), pow(10, 5))
    # q = generate_prime(pow(10, 3), pow(10, 5))
    p = int(input("Enter the value of p : "))
    q = int(input("Enter the value of q : "))
    n = p * q
    phin = (p - 1) * (q - 1)
    # e = key_generate(phin)
    e = int(input("Enther the value of e : "))
    d = power(e, -1, phin)
    print(f"The value of d (private key using inverse mod of e) : {d}")
    client_socket, client_addr = server_socket.accept()
    print(f"Public Key : \n e : {e} \n n : {n}")
    client_socket.send(json.dumps([e, n]).encode())
    # Receive the encrypted message.
    encrypted = json.loads(client_socket.recv(1024).decode())
    msg = decrypt(encrypted, d, n)
    print(f"Message : {msg}")
    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    server()
