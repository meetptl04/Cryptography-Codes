import socket

def power(a,b,c):
    return pow(a,b,c)

def client():
    socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket_client.connect(('localhost',8080))
    P,G,Ya = map(int,socket_client.recv(1024).decode().split(','))
    print(f"Public Key of Server : {Ya}")
    Xb = 233
    Yb = power(G,Xb,P)
    print(f"Public Key of Client : {Yb}")
    socket_client.send(f"{Yb}".encode())
    print("Public Key Sent")
    Kb = power(Ya,Xb,P)
    print(f"Shared Key : {Kb}")

if __name__ == '__main__':
    client()
