import socket

def rail_fence_encrypt(text, rails):
    if rails <= 1:
        return text

    fence, rail, direction = [''] * rails, 0, 1
    for char in text:
        fence[rail] += char
        rail += direction
        if rail == rails - 1 or rail == 0:
            direction *= -1

    return ''.join(fence)

def client():
    s = socket.socket()
    s.connect(('localhost', 8080))
    key = int(input("Enter the Key (1-5): "))
    msg = input("Enter message: ")
    encrypted = rail_fence_encrypt(msg, key)
    print(f"Encrypted: {encrypted}")
    s.send(str(key).encode())  # Send key first
    s.send(encrypted.encode())  # Send encrypted message
    s.close()

client()
