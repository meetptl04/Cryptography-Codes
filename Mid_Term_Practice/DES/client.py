# import socket
# from Crypto.Cipher import DES
#
# def pad(text):
#     while len(text) % 8 != 0:
#         text += b' '
#     return text
#
# def encrypt(plaintext, key):
#     cipher = DES.new(key, DES.MODE_ECB)
#     return cipher.encrypt(pad(plaintext))
#
# # Set up the client
# host = '127.0.0.1'
# port = 12345
#
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((host, port))
#
# # Receive the key from the server
# key = client_socket.recv(8)
#
# while True:
#     message = input("Enter message to encrypt (or 'quit' to exit): ")
#     if message.lower() == 'quit':
#         break
#     encrypted_message = encrypt(message.encode(), key)
#     client_socket.send(encrypted_message)
#
# client_socket.close()


import socket
from Crypto.Cipher import DES

def encrypt(plaintext, key):
    return DES.new(key, DES.MODE_ECB).encrypt(plaintext.ljust(8 * ((len(plaintext) + 7) // 8)))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))
key = client.recv(8)

while True:
    msg = input("Message (or 'quit'): ")
    if msg.lower() == 'quit': break
    client.send(encrypt(msg.encode(), key))

client.close()
