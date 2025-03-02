# enigma_block.py - Lightweight Enigma-Inspired Block Cipher

def simple_sbox(byte):
    """A simple substitution function mimicking a rotor."""
    return ((byte * 7 + 3) % 256)  # Improved nonlinearity

def simple_sbox_inv(byte):
    """Inverse of the simple S-box."""
    for i in range(256):
        if simple_sbox(i) == byte:
            return i
    return byte  # Fallback

def feistel_round(left, right, key):
    """A lightweight Feistel round with improved mixing."""
    new_right = left ^ simple_sbox((right ^ key) & 0xFF)
    return right, new_right

def feistel_round_inv(left, right, key):
    """Inverse Feistel round."""
    new_left = right ^ simple_sbox_inv((left ^ key) & 0xFF)
    return new_left, right

def encrypt_block(block, key, rounds=6):
    """Encrypts a 32-bit block with a 128-bit key."""
    left, right = (block >> 16) & 0xFFFF, block & 0xFFFF
    keys = [(key >> (i * 16)) & 0xFFFF for i in range(rounds)]
    for k in keys:
        left, right = feistel_round(left, right, k)
    return (left << 16) | right

def decrypt_block(block, key, rounds=6):
    """Decrypts a 32-bit block."""
    left, right = (block >> 16) & 0xFFFF, block & 0xFFFF
    keys = [(key >> (i * 16)) & 0xFFFF for i in range(rounds)][::-1]
    for k in keys:
        left, right = feistel_round_inv(left, right, k)
    return (left << 16) | right

def pad(text, block_size=4):
    """Pads the text to fit block size."""
    padding = block_size - (len(text) % block_size)
    return text + bytes([padding] * padding)

def unpad(text):
    """Removes padding."""
    if text[-1] <= len(text):
        return text[:-text[-1]]
    return text

def encrypt(text, key):
    """Encrypts any length text."""
    text = pad(text.encode())
    encrypted_blocks = [encrypt_block(int.from_bytes(text[i:i+4], 'big'), key) for i in range(0, len(text), 4)]
    return b''.join(block.to_bytes(4, 'big') for block in encrypted_blocks)

def decrypt(ciphertext, key):
    """Decrypts ciphertext back to original text."""
    decrypted_blocks = [decrypt_block(int.from_bytes(ciphertext[i:i+4], 'big'), key) for i in range(0, len(ciphertext), 4)]
    return unpad(b''.join(block.to_bytes(4, 'big') for block in decrypted_blocks)).decode(errors='ignore')
