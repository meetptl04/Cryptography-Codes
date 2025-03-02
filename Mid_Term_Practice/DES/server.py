# import socket
# from Crypto.Cipher import DES
# from secrets import token_bytes
#
# def pad(text):
#     while len(text) % 8 != 0:
#         text += b' '
#     return text
#
# def decrypt(ciphertext, key):
#     cipher = DES.new(key, DES.MODE_ECB)
#     return cipher.decrypt(ciphertext).rstrip(b' ')
#
# # Generate a random 8-byte key
# key = token_bytes(8)
#
# # Set up the server
# host = '127.0.0.1'
# port = 12345
#
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((host, port))
# server_socket.listen(1)
#
# print("Server is waiting for connections...")
#
# client_socket, addr = server_socket.accept()
# print(f"Connected to {addr}")
#
# # Send the key to the client
# client_socket.send(key)
#
# while True:
#     encrypted_message = client_socket.recv(1024)
#     if not encrypted_message:
#         break
#     decrypted_message = decrypt(encrypted_message, key)
#     print(f"Received message: {decrypted_message.decode()}")
#
# client_socket.close()
# server_socket.close()


import socket
from Crypto.Cipher import DES
from secrets import token_bytes

def decrypt(ciphertext, key):
    return DES.new(key, DES.MODE_ECB).decrypt(ciphertext).rstrip(b' ')

key = token_bytes(8)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 12345))
server.listen(1)

print("Server waiting...")
client, addr = server.accept()
client.send(key)

while True:
    msg = client.recv(1024)
    if not msg: break
    print(f"Received: {decrypt(msg, key).decode()}")

client.close()
server.close()
