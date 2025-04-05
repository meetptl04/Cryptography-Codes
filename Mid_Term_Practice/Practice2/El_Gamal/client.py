import socket
import json

def power(a, b, c):
    return pow(a, b, c)

def encrypt(q, g, Ya, msg):
    # k = random.randint(2, q - 1)  # Choose random k
    k = 1111
    c2 = []
    c1 = power(g, k, q)
    temp = power(Ya, k, q)
    for i in range(0, len(msg)):
        c2.append(temp * ord(msg[i]))
    return c1, c2

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))
    q, g, Ya = map(int, client_socket.recv(1024).decode().split(','))
    print(f"El_Gamal Public Key: \n q: {q} \n g: {g} \n Ya: {Ya}")
    msg = input("Enter the message:")
    C1, C2 = encrypt(q, g, Ya, msg)
    data = json.dumps([C1, C2])
    client_socket.send(data.encode())
    print("Message Sent")
    client_socket.close()

if __name__ == '__main__':
    client()
