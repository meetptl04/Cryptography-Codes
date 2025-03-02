# Alice's Code
import socket

# Power function to return value of a^b mod P
def power(a, b, p):
    return pow(a, b, p)

def client():
    # Connect to the attacker (instead of server)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8081))  # Connect to attacker on port 8081

    # Receive public values G and P from the attacker (MITM)
    P_G_message = client_socket.recv(1024).decode()
    P, G = map(int, P_G_message.split())

    print("The value of P:", P)
    print("The value of G:", G)

    # Client chooses the private key a
    a = 4  # Alice's private key
    # a = 227  # Alice's private key
    print("The private key a for Client (Alice):", a)

    # Gets the generated key (x = G^a mod P)
    x = power(G, a, P)

    # Send the generated key (x) to the attacker (instead of the server)
    client_socket.send(f"{x}".encode())

    # Receive the server's public key (y') from the attacker
    y_prime = int(client_socket.recv(1024).decode())
    print("Received modified public key (y') from Attacker:", y_prime)

    # Generate the secret key (ka = y'^a mod P)
    ka = power(y_prime, a, P)  # Secret key for Client (Alice)
    print("Secret key for Client (Alice):", ka)

    # Send the secret key to the attacker (to verify)
    client_socket.send(f"{ka}".encode())

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    client()
