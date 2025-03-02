import socket

def server():
    host , port = 'localhost' , 12345

    # Create socket
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server_socket:
        # Bind socker to address
        server_socket.bind((host,port))
        server_socket.listen()
        print(f"Server is listening on {host} : {port}...")

        # Accept the connetion
        conn , addr = server_socket.accept()

        with conn :
            print(f"Connected by {addr}")

            data = conn.recv(1024) # Buffer Size
            print(f"Received Message : {data.decode()}")

            response = "Message received successfully"
            conn.sendall(response.encode())

if __name__ == "__main__":
    server()