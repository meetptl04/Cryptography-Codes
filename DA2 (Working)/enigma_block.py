def simple_sbox(byte):
    """A simple substitution function mimicking a rotor."""
    return ((byte * 7 + 3) % 256)  # Improved nonlinearity


def simple_sbox_inv(byte):
    """Inverse of the simple S-box (unused in the Feistel decryption)."""
    for i in range(256):
        if simple_sbox(i) == byte:
            return i
    return byte  # Fallback


def feistel_round(left, right, key):
    """A lightweight Feistel round with improved mixing."""
    new_right = left ^ simple_sbox((right ^ key) & 0xFF)
    return right, new_right


def feistel_round_inv(left, right, key):
    """
    Inverse Feistel round.

    In a Feistel cipher the decryption round is computed by reversing the order
    and applying the same function F. Here, we use simple_sbox (and not its inverse)
    so that given (L, R) = (R_old, L_old XOR F(R_old, key)) we recover the original pair.
    """
    new_left = right ^ simple_sbox((left ^ key) & 0xFF)
    return new_left, left


def encrypt_block(block, key, rounds=4):
    """
    Encrypts a 32-bit block with a 64-bit key.

    We use 4 rounds (4 * 16 = 64 bits) to extract 16-bit round keys.
    """
    left, right = (block >> 16) & 0xFFFF, block & 0xFFFF
    # Extract subkeys: one 16-bit block per round
    keys = [(key >> (i * 16)) & 0xFFFF for i in range(rounds)]
    for k in keys:
        left, right = feistel_round(left, right, k)
    return (left << 16) | right


def decrypt_block(block, key, rounds=4):
    """
    Decrypts a 32-bit block with a 64-bit key.

    The round keys are applied in reverse order.
    """
    left, right = (block >> 16) & 0xFFFF, block & 0xFFFF
    keys = [(key >> (i * 16)) & 0xFFFF for i in range(rounds)][::-1]
    for k in keys:
        left, right = feistel_round_inv(left, right, k)
    return (left << 16) | right


def pad(text, block_size=4):
    """Pads the text to fit the block size using PKCS#7 padding."""
    padding = block_size - (len(text) % block_size)
    return text + bytes([padding] * padding)


def unpad(text):
    """Removes padding."""
    return text[:-text[-1]]


def encrypt(text, key):
    """Encrypts any length text."""
    padded = pad(text.encode())
    encrypted_blocks = [
        encrypt_block(int.from_bytes(padded[i:i + 4], 'big'), key)
        for i in range(0, len(padded), 4)
    ]
    return b''.join(block.to_bytes(4, 'big') for block in encrypted_blocks)


def decrypt(ciphertext, key):
    """Decrypts ciphertext back to the original text."""
    decrypted_blocks = [
        decrypt_block(int.from_bytes(ciphertext[i:i + 4], 'big'), key)
        for i in range(0, len(ciphertext), 4)
    ]
    decrypted = b''.join(block.to_bytes(4, 'big') for block in decrypted_blocks)
    return unpad(decrypted).decode(errors='ignore')
