import socket
from DSS import verify, print_key

def run_server():
    sock = socket.socket()
    sock.bind(("localhost", 9999))
    sock.listen(1)
    print("DSS Server ready")

    conn, addr = sock.accept()
    print(f"Connection from {addr}")

    # Get public key
    pub_data = conn.recv(1024).decode()
    p, q, g, y = map(int, pub_data.split('|')[1:])
    pub_key = (p, q, g, y)
    print("Client public key:")
    print_key("P", p)
    print_key("Q", q)
    print_key("G", g)
    print_key("Y", y)

    # Get file info
    file_info = conn.recv(1024).decode().split('|')
    fname, r, s = file_info[1], int(file_info[2]), int(file_info[3])
    print(f"\nReceiving {fname} with signature:")
    print_key("R", r)
    print_key("S", s)

    # Receive file
    data = b""
    while True:
        chunk = conn.recv(4096)
        if not chunk: break
        data += chunk
    print(f"Received {len(data)} bytes")

    # Verify
    valid = verify(data, (r,s), pub_key)
    print(f"\nVerification {'SUCCEEDED' if valid else 'FAILED'}")

    conn.close()
    sock.close()

if __name__ == "__main__":
    run_server()
