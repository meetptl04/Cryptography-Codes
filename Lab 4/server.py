import socket
import threading
import pickle
from aes import AES

PORT = 5000
SERVER = 'localhost'


def handle_client(client_socket, addr, aes_instance):
    """Handle individual client connection - now only decrypts received ciphertext"""
    print(f"Client connected: {addr}")

    try:
        while True:
            try:
                # Receive encrypted data and key from client
                ciphertext = pickle.loads(client_socket.recv(4096))
                key = pickle.loads(client_socket.recv(4096))

                # Check for exit condition
                if len(ciphertext) == 0:
                    break

                # Decrypt the received ciphertext
                decrypted = aes_instance.decrypt(ciphertext, key)
                print(f"Decryption completed for client: {addr}")

                # Send decrypted result back to client
                client_socket.send(pickle.dumps(decrypted))

            except EOFError:
                break
            except Exception as e:
                print(f"Error processing client request: {str(e)}")
                break

    except Exception as e:
        print(f"Error handling client: {str(e)}")
    finally:
        client_socket.close()
        print(f"Client disconnected: {addr}")


def start_server():
    """Start the AES server"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER, PORT))
    server_socket.listen()

    print(f"Server started on port {PORT}")

    # Create a single AES instance to be shared among clients
    aes_instance = AES()

    try:
        while True:
            client_socket, addr = server_socket.accept()

            # Create a new thread for each client
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, addr, aes_instance)
            )
            thread.start()
            print(f"Active connections: {threading.active_count() - 1}")

    except KeyboardInterrupt:
        print("\nServer shutting down...")
    except Exception as e:
        print(f"Server error: {str(e)}")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()