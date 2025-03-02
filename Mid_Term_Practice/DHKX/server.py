# Alice

import socket

def power(a,b,p):
    return pow(a,b,p) # a^b mod p

def server():
    # P : prime number
    # G : primitive root
    # a : private key
    # x = G^a mod P

    P, G , a = 23 , 9 , 3
    print(f"The value of P is : {P}\n The value of its primitive root G is : {G}\n The value of Alice's private ket is : {a}")

    x = power(G,a,P) # x = G^a mod P
    print(f"The generated key value for Alice is X : {x}")

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(('localhost',8080))
    server_socket.listen(1)

    print(f"Waiting for client to connect ....")
    client_socket , client_addr = server_socket.accept()
    print(f"Client {client_addr} connected")

    client_socket.send(f"{G} {P}".encode())

    y = int(client_socket.recv(1024).decode())
    print(f"Public Key received by server from the client : {y}")

    ka = power(G,y,P)
    print(f"The received private key ka : {ka}")

    client_socket.send(f"{x}".encode())

    client_socket.close()


if __name__ == "__main__" :
    server()