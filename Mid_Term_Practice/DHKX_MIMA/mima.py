import socket

def power(a,b,c):
    return pow(a,b,c)

def mima():
    print(f"Waiting to client to connect....")

    # Attacker to server (actual) as a client
    att_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    att_server_socket.connect(('localhost',8080))

    # Attacker to client (actual) as a server
    att_client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    att_client_socket.bind(('localhost',8081))
    att_client_socket.listen(1)

    client_socket , client_addr = att_client_socket.accept()
    print(f"Client {client_addr} connected.")

    # P_G msg from server
    P_G_msg = att_server_socket.recv(1024).decode()
    print(f"Intercepted P and G from the server : {P_G_msg}")
    client_socket.send(P_G_msg.encode())
    P,G = map(int,P_G_msg.split())

    # Attacker's Dummy values

    a_prime = 6 # Dummy private key for server
    b_prime = 5 # Dummy private ket for client

    x_prime = power(G,a_prime,P) # att_to_client
    y_prime = power(G,b_prime,P) # att_to_server

    # Shared to server
    y = int(client_socket.recv(1024).decode())
    print(f"Intercepted Client's public key (y) : {y}")
    att_server_socket.send(f"{y_prime}".encode())
    print(f"Attacker's public key for server : {y_prime}")

    # Shared to client
    x = int(att_server_socket.recv(1024).decode())
    print(f"Intercepted Server's public key (x) : {x}")
    client_socket.send(f"{x_prime}".encode())
    print(f"Attacker's public key for client : {x_prime}")

    ka = power(x_prime,b_prime,P) # att_new_key_for_client
    kb = power(y_prime,a_prime,P) # attt_new_key_for_server

    att_server_socket.close()
    client_socket.close()

if __name__ == '__main__':
    mima()







