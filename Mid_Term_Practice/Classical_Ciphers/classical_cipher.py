import numpy as np
from math import gcd


# ------------------ Helper Functions ------------------
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)


def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError("No modular inverse exists")
    else:
        return x % m


# ------------------ Caesar Cipher ------------------
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


# ------------------ Playfair Cipher ------------------
def generate_playfair_table(key):
    key = key.upper().replace("J", "I")
    table = []
    for char in key:
        if char not in table and char.isalpha():
            table.append(char)
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in table:
            table.append(ch)
    return [table[i * 5:(i + 1) * 5] for i in range(5)]

def playfair_process(text):
    text = text.upper().replace("J", "I").replace(" ", "")
    prepared = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = ""
        if i + 1 < len(text):
            b = text[i + 1]
        if b == "" or a == b:
            prepared += a + "X"
            i += 1
        else:
            prepared += a + b
            i += 2
    return prepared

def playfair_encrypt(text, key):
    table = generate_playfair_table(key)
    pos = {}
    for i in range(5):
        for j in range(5):
            pos[table[i][j]] = (i, j)
    text = playfair_process(text)
    cipher = ""
    for i in range(0, len(text), 2):
        a = text[i]
        b = text[i + 1]
        row1, col1 = pos[a]
        row2, col2 = pos[b]
        if row1 == row2:
            cipher += table[row1][(col1 + 1) % 5]
            cipher += table[row2][(col2 + 1) % 5]
        elif col1 == col2:
            cipher += table[(row1 + 1) % 5][col1]
            cipher += table[(row2 + 1) % 5][col2]
        else:
            cipher += table[row1][col2]
            cipher += table[row2][col1]
    return cipher

def playfair_decrypt(cipher, key):
    table = generate_playfair_table(key)
    pos = {}
    for i in range(5):
        for j in range(5):
            pos[table[i][j]] = (i, j)
    text = ""
    for i in range(0, len(cipher), 2):
        a = cipher[i]
        b = cipher[i + 1]
        row1, col1 = pos[a]
        row2, col2 = pos[b]
        if row1 == row2:
            text += table[row1][(col1 - 1) % 5]
            text += table[row2][(col2 - 1) % 5]
        elif col1 == col2:
            text += table[(row1 - 1) % 5][col1]
            text += table[(row2 - 1) % 5][col2]
        else:
            text += table[row1][col2]
            text += table[row2][col1]
    # Remove 'X' that were added during encryption
    text = text.replace("XX", "X")  # Handle double 'X'
    while "X" in text and len(text) > 1 and text[-1] == "X":
        text = text[:-1]
    return text


# ------------------ Hill Cipher (3x3 matrix) ------------------
def is_valid_hill_key(key_matrix):
    det = int(round(np.linalg.det(key_matrix)))
    det_mod = det % 26
    if det_mod == 0:
        return False
    return gcd(det_mod, 26) == 1


def hill_encrypt(text, key):
    text = text.upper().replace(" ", "")
    n = 3
    text += 'X' * ((n - len(text) % n) % n)
    key_matrix = np.array([ord(c.upper()) - ord('A') for c in key[:n * n]]).reshape(n, n)
    if not is_valid_hill_key(key_matrix):
        raise ValueError("Invalid key matrix - must be invertible modulo 26")
    encrypted = []
    # for i in range(0, len(text), n):
    #     block = [ord(c) - ord('A') for c in text[i:i + n]]
    #     vec = np.array(block).reshape(n, 1)
    #     encrypted_vec = np.dot(key_matrix, vec) % 26
    #     encrypted += [chr(v + ord('A')) for v in encrypted_vec.flatten()]
    # return ''.join(encrypted)
    # Vectorized encryption
    text_num = np.array([ord(c)-65 for c in text])
    encrypted = (key_matrix @ text_num.reshape(n,-1, order='F')) % 26
    return ''.join([chr(c+65) for c in encrypted.ravel('F')])


def hill_decrypt(ciphertext, key):
    n = 3
    key_matrix = np.array([ord(c.upper()) - ord('A') for c in key[:n * n]]).reshape(n, n)
    det = int(round(np.linalg.det(key_matrix))) % 26
    det_inv = mod_inverse(det, 26)
    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            minor = np.delete(np.delete(key_matrix, i, axis=0), j, axis=1)
            adj[i][j] = ((-1) ** (i + j)) * int(round(np.linalg.det(minor)))
    inverse_matrix = (det_inv * adj.T) % 26
    decrypted = []
    for i in range(0, len(ciphertext), n):
        block = [ord(c) - ord('A') for c in ciphertext[i:i + n]]
        vec = np.array(block).reshape(n, 1)
        decrypted_vec = np.dot(inverse_matrix, vec) % 26
        decrypted += [chr(v + ord('A')) for v in decrypted_vec.flatten()]
    return ''.join(decrypted).rstrip('X')


# ------------------ Vigenère Cipher ------------------
def vigenere_encrypt(text, key):
    text = text.upper()
    key = key.upper()
    result = ""
    key_length = len(key)
    for i, char in enumerate(text):
        if char.isalpha():
            shift = ord(key[i % key_length]) - ord('A')
            result += chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
        else:
            result += char
    return result


def vigenere_decrypt(cipher, key):
    cipher = cipher.upper()
    key = key.upper()
    result = ""
    key_length = len(key)
    for i, char in enumerate(cipher):
        if char.isalpha():
            shift = ord(key[i % key_length]) - ord('A')
            result += chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
        else:
            result += char
    return result


# ------------------ Rail Fence Cipher ------------------
def rail_fence_encrypt(text, rails):
    if rails <= 1:
        return text
    fence = ['' for _ in range(rails)]
    rail = 0
    direction = 1
    for char in text:
        fence[rail] += char
        rail += direction
        if rail == rails - 1 or rail == 0:
            direction *= -1
    return ''.join(fence)


def rail_fence_decrypt(cipher, rails):
    if rails <= 1:
        return cipher
    pattern = []
    rail = 0
    direction = 1
    for i in range(len(cipher)):
        pattern.append(rail)
        rail += direction
        if rail == rails - 1 or rail == 0:
            direction *= -1
    rail_counts = [pattern.count(r) for r in range(rails)]
    rails_text = []
    index = 0
    for count in rail_counts:
        rails_text.append(list(cipher[index:index + count]))
        index += count
    result = ""
    for r in pattern:
        result += rails_text[r].pop(0)
    return result


# ------------------ Row Transposition Cipher ------------------
def row_transposition_encrypt(text, key):
    cols = len(key)
    rows = len(text) // cols
    if len(text) % cols != 0:
        rows += 1
    text += "X" * (rows * cols - len(text))
    matrix = [list(text[i * cols:(i + 1) * cols]) for i in range(rows)]
    order = sorted(list(enumerate(key)), key=lambda x: x[1])
    ciphertext = ""
    for index, _ in order:
        for row in matrix:
            ciphertext += row[index]
    return ciphertext


def row_transposition_decrypt(cipher, key):
    cols = len(key)
    rows = len(cipher) // cols
    order = sorted(list(enumerate(key)), key=lambda x: x[1])
    matrix = [[''] * cols for _ in range(rows)]
    index = 0
    for col_index, _ in order:
        for r in range(rows):
            matrix[r][col_index] = cipher[index]
            index += 1
    plaintext = ''.join(''.join(row) for row in matrix)
    return plaintext.rstrip("X")


# Main Program
if __name__ == "__main__":
    print("Choose a cipher from: caesar, playfair, hill, vigenere, rail_fence, row_transposition")
    cipher_type = input("Cipher: ").strip()
    text = input("Text: ").strip()
    key = input(
        "Key (for caesar or rail_fence, enter a number; for hill at least 9 characters; for row_transposition enter a key string): ").strip()

    if cipher_type == "caesar":
        shift = int(key)
        encrypted = caesar_encrypt(text, shift)
        decrypted = caesar_decrypt(encrypted, shift)
    elif cipher_type == "playfair":
        encrypted = playfair_encrypt(text, key)
        decrypted = playfair_decrypt(encrypted, key)
    elif cipher_type == "hill":
        encrypted = hill_encrypt(text, key)
        decrypted = hill_decrypt(encrypted, key)
    elif cipher_type == "vigenere":
        encrypted = vigenere_encrypt(text, key)
        decrypted = vigenere_decrypt(encrypted, key)
    elif cipher_type == "rail_fence":
        rails = int(key)
        encrypted = rail_fence_encrypt(text, rails)
        decrypted = rail_fence_decrypt(encrypted, rails)
    elif cipher_type in ["row_transposition", "rowtransposition"]:
        encrypted = row_transposition_encrypt(text, key)
        decrypted = row_transposition_decrypt(encrypted, key)
    else:
        encrypted = "Invalid cipher type"
        decrypted = ""

    print("Encrypted Text:", encrypted)
    print("Decrypted Text:", decrypted)
