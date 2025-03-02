import socket


def server():
    # Server configuration
    host = 'localhost'
    port = 12345

    # Create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind socket to address
        server_socket.bind((host, port))
        # Listen for connections
        server_socket.listen()
        print(f"Server listening on {host}:{port}...")

        # Accept connection
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")

            # Receive data
            data = conn.recv(1024)
            print(f"Received message: {data.decode()}")

            # Send response
            response = "Message received successfully"
            conn.sendall(response.encode())


if __name__ == "__main__":
    server()
