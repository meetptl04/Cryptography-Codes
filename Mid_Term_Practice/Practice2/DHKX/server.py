import socket

def power(a,b,c):
    return pow(a,b,c)

def server():
    P,G,Xa = 353 , 3 , 97
    Ya = power(G,Xa,P)
    print(f"Public Key of Server : {Ya}")
    socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket_server.bind(('localhost',8080))
    socket_server.listen(1)
    
    client_socket , client_addr = socket_server.accept()
    print(f"Connection from {client_addr}")
    client_socket.send(f"{P},{G},{Ya}".encode())
    print("Public Key Sent")
    Yb = int(client_socket.recv(1024).decode())
    print(f"Public Key of Client : {Yb}")
    Ka = power(Yb,Xa,P)
    print(f"Shared Key : {Ka}")

if __name__ == '__main__':
    server() 

