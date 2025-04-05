import socket
import json

def power(a, b, c):
    return pow(a, b, c)

def encrypt(msg, e, n):
    encry = []
    for i in range(len(msg)):
        encry.append(power(ord(msg[i]), e, n))
    return encry

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))
    print(f"Yeah , I am Client : Hahahaha")
    # Receive the public key.
    e, n = json.loads(client_socket.recv(1024).decode())
    print(f"Public Key Received: \n e: {e} \n n: {n}")
    msg = input("Enter the message: ")
    encrypted = encrypt(msg, e, n)
    print(f"Encrypted Text: {encrypted}")
    # Send the encrypted message as JSON.
    client_socket.send(json.dumps(encrypted).encode())
    print("Message Sent")
    client_socket.close()

if __name__ == '__main__':
    client()
