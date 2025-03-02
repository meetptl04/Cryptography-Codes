import socket
from md5 import md5_hash

HOST = '127.0.0.1'
PORT = 65432

print(f"Starting MD5 verification server on {HOST}:{PORT}")

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
            
            print(f"\nReceived data from client: \n{data}")
            message, client_hash = data.split('|')
            print(f"Extracted message: \n'{message}'")
            print(f"Received hash from client: \n{client_hash}")
            
            server_hash = md5_hash(message)
            print(f"Calculated hash on server: \n{server_hash}")
            
            if server_hash == client_hash:
                response = f"Message integrity verified. \nHash: {server_hash}"
                print("Integrity check: PASSED")
            else:
                response = f"Message integrity compromised. \nExpected: {server_hash}, \nReceived: {client_hash}"
                print("Integrity check: FAILED")
            
            print(f"Sending response to client: \n{response}")
            conn.sendall(response.encode())

print("Server shutting down.")
