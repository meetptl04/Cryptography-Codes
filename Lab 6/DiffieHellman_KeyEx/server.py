import socket

def power(a, b, p):
    return pow(a, b, p)   #a^b mod P

def server():
    P = 23  # prime number P
    print("The value of P:", P)

    G = 9  # A primitive root for P
    print("The value of G:", G)

    # Server chooses the private key b
    b = 3  # Bob's private key
    print("The private key b for Server (Bob) (b) :", b)

    # Gets the generated key (y = G^b mod P)
    y = power(G, b, P)

    # Set up the server to listen for a connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))  # Bind to localhost on port 8080
    server_socket.listen(1)  # Start listening for incoming connections

    print("Waiting for client to connect...")
    client_socket, client_address = server_socket.accept()  # Accept the connection
    print(f"Client {client_address} connected.")

    # Send public values G and P to the client
    client_socket.send(f"{G} {P}".encode())

    # Receive the client's public key (x = G^a mod P)
    x = int(client_socket.recv(1024).decode())

    # Generate the secret key (ka = x^b mod P)
    ka = power(x, b, P)  # Secret key for Server (Bob)
    print("Secret key for Server is (ka ):", ka)

    # Send the server's public key (y) to the client
    client_socket.send(f"{y}".encode())

    # Receive the secret key from the client
    kb = int(client_socket.recv(1024).decode())  # This should be the same secret key
    print("Secret key for Client (received by server) is (kb) :", kb)

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    server()

