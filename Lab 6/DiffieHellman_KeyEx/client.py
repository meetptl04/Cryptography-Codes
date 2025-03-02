import socket

# Power function to return value of a^b mod P
def power(a, b, p):
    return pow(a, b, p)

# Main function
def client():
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))  # Connect to server on localhost:8080

    # Receive public values G and P from the server
    G, P = map(int, client_socket.recv(1024).decode().split())
    print("The value of P:", P)
    print("The value of G:", G)

    # Client chooses the private key a
    a = 4  # Alice's private key
    print("The private key a for Client (Alice)(a):", a)

    # Gets the generated key (x = G^a mod P)
    x = power(G, a, P)

    # Send the generated key (x) to the server
    client_socket.send(f"{x}".encode())

    # Receive the server's public key (y = G^b mod P)
    y = int(client_socket.recv(1024).decode())

    # Generate the secret key (ka = y^a mod P)
    ka = power(y, a, P)  # Secret key for Client (Alice)
    print("Secret key for Client is (ka):", ka)

    # Send the secret key to the server (this is a way to verify the keys match)
    client_socket.send(f"{ka}".encode())

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    client()
