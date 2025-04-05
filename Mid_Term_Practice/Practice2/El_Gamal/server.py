import socket
import random
import json

def power(a, b, c):
    return pow(a, b, c)

def key_generate(q):
    return random.randint(2, q - 1)

def decrypt(q, key, C1, C2):
    temp = power(C1, key, q) 
    msg = ""
    for i in range(0, len(C2)):
        msg += chr(int(C2[i] // temp))
    return msg

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080)) 
    server_socket.listen(1)

    q = random.randint(pow(10, 20), pow(10, 50)) 
    g = random.randint(2, q)  # E1
    # key = key_generate(q)  # Private key
    key = random.randint(2, q - 1) # Private key
    Ya = power(g, key, q)  # E2
    print(f"q: {q} \n g: {g} \n Ya : {Ya} \n key: {key}")
    client_socket, client_addr = server_socket.accept()
    print(f"Connection from {client_addr}")
    client_socket.send(f"{q},{g},{Ya}".encode())
    print("Public Key Sent")
    # Receive encrypted data
    data = json.loads(client_socket.recv(1024).decode())
    C1, C2 = data
    print(f"C1: {C1} \n C2: {C2}")
    msg = decrypt(q, key, C1, C2)
    print(f"Message: {msg}")
    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    server()
