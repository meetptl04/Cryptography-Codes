import socket
from sha512 import sha512_hash

HOST = '127.0.0.1'
PORT = 65432

print(f"Connecting to SHA512 verification server at {HOST}:{PORT}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to server.")
    
    while True:
        message = input("\nEnter a message (or 'quit' to exit): ")
        print("\n")
        if message.lower() == 'quit':
            print("Exiting...")
            break
        
        hash_value = sha512_hash(message)
        print(f"Calculated SHA512 hash: \n{hash_value}\n")
        
        data_to_send = f"{message}|{hash_value}"
        print(f"Sending to server: \n{data_to_send}\n")
        s.sendall(data_to_send.encode())
        
        data = s.recv(1024)
        print(f"Server response: \n{data.decode()}\n")

print("Client disconnected.")
