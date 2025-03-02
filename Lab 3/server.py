import socket
from des import (des_decrypt,des_encrypt)
s=socket.socket()

s.bind(("localhost",9999))

s.listen(1)

print("Server is listening")

key="AABB09182736CCDD"

while True:
    c,addr=s.accept()
    print("Connected with",addr)
    cypher=c.recv(1024)
    print("Cypher code recieved from the client: ",cypher.decode())
    plaintext=des_decrypt(cypher.decode(),key)
    print("The decyphered plaintext is: ",plaintext)