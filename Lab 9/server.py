import socket
from sha512 import sha512_hash

HOST = '127.0.0.1'
PORT = 65432

print(f"Starting SHA512 verification server on {HOST}:{PORT}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server is listening for connections...")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by client at {addr}")
        while True:
            data = conn.recv(1024).decode()
            if not data:
                print("Client disconnected.")
                break
            
            print(f"\nReceived data from client: \n{data}\n")
            message, client_hash = data.split('|')
            print(f"Extracted message: \n'{message}'\n")
            print(f"Received hash from client: \n{client_hash}\n")
            
            server_hash = sha512_hash(message)
            print(f"Calculated hash on server: \n{server_hash}\n")
            
            if server_hash == client_hash:
                print("Received Hash == Calculated Hash\n")
                response = f"Message integrity verified. \nHash: {server_hash}\n"
                
                print("Integrity check: PASSED")
            else:
                response = f"Message integrity compromised. \nExpected: {server_hash}, \nReceived: {client_hash}"
                print("Integrity check: FAILED")
            
            print(f"Sending response to client: \n{response}\n")
            conn.sendall(response.encode())

print("Server shutting down.")
