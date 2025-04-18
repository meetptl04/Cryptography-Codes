import socket
from enigma_block import decrypt


def server():
    host, port = 'localhost', 12345
    key = 0xA3B1C2D3E4F56789  # 64-bit key for simplicity

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("Server listening...")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            ciphertext = conn.recv(1024)

            # Added print statement to show the received encrypted text in hexadecimal format
            print("Received encrypted text (Hex):", ciphertext.hex())

            decrypted_text = decrypt(ciphertext, key)
            print("Decrypted at Server:", decrypted_text)

            # conn.sendall(decrypted_text.encode(errors='ignore'))


if __name__ == "__main__":
    server()
