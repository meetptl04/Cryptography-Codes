# BOB

import socket

def power(a,b,c):
    return pow(a,b,c)

def client():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect(('localhost',8080))

    G , P = map(int,client_socket.recv(1024).decode().split())
    b = 4

    y = power(G, b, P)  # y = G^b mod P
    print(f"The generated key for client (BOB) y : {y}")

    client_socket.send(f"{y}".encode())

    x = int(client_socket.recv(1024).decode())
    print(f"Public Key received by client from the server : {x}")

    kb = power(G,x,P)
    print(f"The received private key ka : {kb}")

    # client_socket.send(f"{y}".encode())

    client_socket.close()


if __name__ == "__main__" :
    client()