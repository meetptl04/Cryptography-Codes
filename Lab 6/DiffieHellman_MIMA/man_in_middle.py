import socket

# Power function to return value of a^b mod P
def power(a, b, p):
    return pow(a, b, p)

def man_in_middle():
    print("Waiting for client to connect...")

    # Attacker listens for a connection from the client (Alice)
    attacker_to_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    attacker_to_client_socket.bind(('localhost', 8081))  # Attacker listens on port 8081
    attacker_to_client_socket.listen(1)

    client_socket, client_address = attacker_to_client_socket.accept()
    print(f"Client {client_address} connected.")

    # Attacker connects to the actual server (Bob)
    attacker_to_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    attacker_to_server_socket.connect(('localhost', 8080))  # Connect to Bob

    # Intercept P and G from the server
    P_G_message = attacker_to_server_socket.recv(1024).decode()
    print("Intercepted P and G from Server:", P_G_message)

    # Forward P and G to the client (pretending to be the server)
    client_socket.send(P_G_message.encode())

    # Extract P and G
    P, G = map(int, P_G_message.split())

    # Intercept client's public key (x)
    x = int(client_socket.recv(1024).decode())
    print("Intercepted Client's public key (x):", x)

    # Attacker generates its own public key (x') to deceive the server
    a_prime = 6  # Attacker's private key (random choice)
    # a_prime = 175  # Attacker's private key (random choice)
    x_prime = power(G, a_prime, P)
    print("Attacker's public key to Server (x'):", x_prime)
    attacker_to_server_socket.send(f"{x_prime}".encode())  # Forward fake x' to server

    # Intercept server's public key (y)
    y = int(attacker_to_server_socket.recv(1024).decode())
    print("Intercepted Server's public key (y):", y)

    # Attacker generates its own public key (y') to send to the client
    b_prime = 5  # Attacker's second private key (random choice)
    # b_prime = 65  # Attacker's second private key (random choice)
    y_prime = power(G, b_prime, P)
    print("Attacker's public key to Client (y'):", y_prime)
    client_socket.send(f"{y_prime}".encode())  # Forward fake y' to client

    # Compute shared secrets (so the attacker can decrypt messages)
    ka = power(y_prime, a_prime, P)  # Attacker's shared key with Client
    kb = power(x_prime, b_prime, P)  # Attacker's shared key with Server
    # print("Attacker's secret key with Client (ka):", ka)
    # print("Attacker's secret key with Server (kb):", kb)
    #
    # # Send computed key to the server
    # attacker_to_server_socket.send(f"{ka}".encode())

    # Close connections
    client_socket.close()
    attacker_to_server_socket.close()

if __name__ == "__main__":
    man_in_middle()
