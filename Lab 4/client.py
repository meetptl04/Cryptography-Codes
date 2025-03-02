import socket
import pickle
from aes import AES

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 5000
SAMPLE_KEY = "000102030405060708090a0b0c0d0e0f"


def pad_input(input_bytes):
    """Pad input to 16 bytes"""
    padded = bytearray(16)
    for i in range(min(len(input_bytes), 16)):
        padded[i] = input_bytes[i]
    return bytes(padded)


def main():
    # Create AES instance for encryption and hex conversion
    aes = AES()

    try:
        # Connect to server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

        print("Connected to server")
        print(f"Using sample key: {SAMPLE_KEY}")

        while True:
            # Get user input
            user_input = input("\nEnter plaintext (or 'exit' to quit): ")

            if user_input.lower() == 'exit':
                # Send empty array to signal exit
                client_socket.send(pickle.dumps(b''))
                client_socket.send(pickle.dumps(b''))
                break

            # Prepare the data
            plaintext = pad_input(user_input.encode())
            key = aes.hex_to_bytes(SAMPLE_KEY)

            # Encrypt the data
            encrypted = aes.encrypt(plaintext, key)
            print(f"\nEncrypted (hex): {aes.bytes_to_hex(encrypted)}")

            # Send encrypted data and key to server
            client_socket.send(pickle.dumps(encrypted))
            client_socket.send(pickle.dumps(key))

            # Receive decrypted result from server
            decrypted = pickle.loads(client_socket.recv(4096))

            # Display results
            print("Results:")
            print(f"Original text: {plaintext.decode().strip()}")
            print(f"Decrypted text (from server): {decrypted.decode().strip()}")

    except ConnectionRefusedError:
        print("Error: Could not connect to server. Make sure the server is running.")
    except Exception as e:
        print(f"Client error: {str(e)}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()