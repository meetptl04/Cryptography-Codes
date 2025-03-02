import socket

def client():
    host , port = 'localhost' , 12345

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client_socket :
        client_socket.connect((host,port))
        print(f"Connected to server at {host} : {port}")

        message = "Hello From the client"
        client_socket.sendall(message.encode())
        print(f"Sent Message : {message}")

        response = client_socket.recv(1024)
        print(f"Server response : {response.decode()}")


if __name__ == "__main__":
    client()