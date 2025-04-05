import socket

def rail_fence_decrypt(cipher, rails):
    if rails <= 1:
        return cipher
    
    # Step 1: Create a zigzag pattern
    pattern, rail, direction = [], 0, 1
    for _ in cipher:
        pattern.append(rail)
        rail += direction
        if rail == rails - 1 or rail == 0:
            direction *= -1

    # Step 2: Count characters per rail
    rail_counts = [pattern.count(r) for r in range(rails)]
    
    # Step 3: Fill rails with encrypted text
    rails_text, index = [], 0
    for count in rail_counts:
        rails_text.append(list(cipher[index:index + count]))
        index += count

    # Step 4: Read in correct order
    return "".join(rails_text[r].pop(0) for r in pattern)

def server():
    s = socket.socket()
    s.bind(('localhost', 8080))
    s.listen(1)
    print("Server is running, waiting for client...")
    c, _ = s.accept()
    key = int(c.recv(1024).decode())  # Receive key first
    encrypted = c.recv(1024).decode()  # Receive encrypted message
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {rail_fence_decrypt(encrypted, key)}")
    c.close()
    s.close()

server()
