import socket
from sdes import SimplifiedDES

# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 65432))

print("Type 'exit' to leave the chat.")

# Key setup: client chooses
key_choice = input("Do you want to use the default key? (yes/no): ").strip().lower()

# Send key choice to server
client_socket.send(key_choice.encode())

if key_choice == "no":
    custom_key = input("Enter a 10-bit custom key (e.g., 1010000010): ").strip()
    client_socket.send(custom_key.encode())
    print(f"Client using custom key: {custom_key}")
else:
    print(f"Client using default key: [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]")

# Initialize SDES with the chosen key (based on the client's choice)
key = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0] if key_choice == "yes" else [int(b) for b in custom_key]
sdes = SimplifiedDES(key)
sdes.key_generation()

while True:
    client_message = input("You (plaintext): ")
    if client_message.lower() == "exit":
        client_socket.send("exit".encode())
        print("Exiting the chat.")
        break

    plaintext = [int(b) for b in client_message]
    encrypted_message = sdes.encrypt(plaintext)
    encrypted_message_str = ''.join(map(str, encrypted_message))
    print(f"Encrypted text to send to server: {encrypted_message_str}")
    client_socket.send(encrypted_message_str.encode())

    data = client_socket.recv(1024).decode()
    if data.lower() == "exit":
        print("Server has exited the chat.")
        break

    print(f"Received encrypted text from server: {data}")
    ciphertext = [int(b) for b in data]
    decrypted_response = ''.join(map(str, sdes.decrypt(ciphertext)))
    print(f"Decrypted text: {decrypted_response}")

client_socket.close()
