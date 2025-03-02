import socket


def client():
    # Server configuration to connect to
    host = 'localhost'
    port = 12345

    # Create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to server
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # Send message
        message = "Hello from client!"
        client_socket.sendall(message.encode())
        print(f"Sent message: {message}")

        # Receive response
        response = client_socket.recv(1024)
        print(f"Server response: {response.decode()}")


if __name__ == "__main__":
    client()
