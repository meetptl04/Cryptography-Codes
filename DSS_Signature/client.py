import socket
from DSS import generate_primes, create_keys, sign, print_key


def run_client():
    # Setup
    fname = input("File to send: ")
    p, q = generate_primes(160, 1024)
    pub_key, priv_key = create_keys(p, q)

    print("Generated keys:")
    print_key("P", p)
    print_key("Q", q)
    print_key("Private", priv_key)

    # Connect to server
    sock = socket.socket()
    sock.connect(("localhost", 9999))

    # Send public key
    pub_data = f"PUBKEY|{p}|{q}|{pub_key[2]}|{pub_key[3]}"
    sock.send(pub_data.encode())

    # Sign file
    with open(fname, "rb") as f:
        data = f.read()
    r, s = sign(data, priv_key, p, q, pub_key[2])

    # Send file info
    sock.send(f"FILE|{fname}|{r}|{s}".encode())

    # Send file
    with open(fname, "rb") as f:
        while chunk := f.read(4096):
            sock.send(chunk)
    print("File sent")

    sock.close()


if __name__ == "__main__":
    run_client()
