# def generate_key_matrix(key):
#     key_matrix = [['' for _ in range(5)] for _ in range(5)]
#     used = [False] * 26
#
#     # Replace J with I in the key
#     key = key.upper().replace('J', 'I')
#
#     # Build key string without duplicates
#     key_string = ""
#     for c in key:
#         if c.isalpha() and not used[ord(c) - ord('A')]:
#             key_string += c
#             used[ord(c) - ord('A')] = True
#
#     # Add remaining alphabet
#     for c in range(ord('A'), ord('Z') + 1):
#         if chr(c) != 'J' and not used[c - ord('A')]:
#             key_string += chr(c)
#
#     # Fill the matrix
#     for i in range(25):
#         key_matrix[i // 5][i % 5] = key_string[i]
#
#     return key_matrix
#
#
# def find_position(matrix, char):
#     for i in range(5):
#         for j in range(5):
#             if matrix[i][j] == char:
#                 return [i, j]
#     return None
#
#
# def prepare_text(text):
#     text = ''.join(c for c in text.upper().replace('J', 'I') if c.isalpha())
#     result = ""
#     i = 0
#
#     while i < len(text):
#         if i + 1 < len(text) and text[i] == text[i + 1]:
#             result += text[i] + 'X'
#             i += 1
#         else:
#             result += text[i]
#             i += 1
#
#     # Add padding if needed
#     if len(result) % 2 != 0:
#         result += 'X'
#
#     return result
#
#
# def encrypt(plaintext, key_matrix):
#     plaintext = prepare_text(plaintext)
#     ciphertext = ""
#
#     for i in range(0, len(plaintext), 2):
#         a, b = plaintext[i], plaintext[i + 1]
#         pos_a = find_position(key_matrix, a)
#         pos_b = find_position(key_matrix, b)
#
#         if pos_a[0] == pos_b[0]:  # Same row
#             ciphertext += key_matrix[pos_a[0]][(pos_a[1] + 1) % 5]
#             ciphertext += key_matrix[pos_b[0]][(pos_b[1] + 1) % 5]
#         elif pos_a[1] == pos_b[1]:  # Same column
#             ciphertext += key_matrix[(pos_a[0] + 1) % 5][pos_a[1]]
#             ciphertext += key_matrix[(pos_b[0] + 1) % 5][pos_b[1]]
#         else:  # Rectangle
#             ciphertext += key_matrix[pos_a[0]][pos_b[1]]
#             ciphertext += key_matrix[pos_b[0]][pos_a[1]]
#
#     return ciphertext
#
#
# def decrypt(ciphertext, key_matrix):
#     plaintext = ""
#
#     for i in range(0, len(ciphertext), 2):
#         a, b = ciphertext[i], ciphertext[i + 1]
#         pos_a = find_position(key_matrix, a)
#         pos_b = find_position(key_matrix, b)
#
#         if pos_a[0] == pos_b[0]:  # Same row
#             plaintext += key_matrix[pos_a[0]][(pos_a[1] - 1) % 5]
#             plaintext += key_matrix[pos_b[0]][(pos_b[1] - 1) % 5]
#         elif pos_a[1] == pos_b[1]:  # Same column
#             plaintext += key_matrix[(pos_a[0] - 1) % 5][pos_a[1]]
#             plaintext += key_matrix[(pos_b[0] - 1) % 5][pos_b[1]]
#         else:  # Rectangle
#             plaintext += key_matrix[pos_a[0]][pos_b[1]]
#             plaintext += key_matrix[pos_b[0]][pos_a[1]]
#
#     return plaintext.replace('X', '')
#
#
# def main():
#     print("Enter the key for the Playfair Cipher:")
#     key = input()
#     key_matrix = generate_key_matrix(key)
#
#     print("Select an option:")
#     print("1. Encrypt a message")
#     print("2. Decrypt a message")
#     choice = int(input())
#
#     if choice == 1:
#         print("Enter the plaintext:")
#         plaintext = input()
#         ciphertext = encrypt(plaintext, key_matrix)
#         print("Ciphertext:", ciphertext)
#     elif choice == 2:
#         print("Enter the ciphertext:")
#         ciphertext = input()
#         plaintext = decrypt(ciphertext, key_matrix)
#         print("Plaintext:", plaintext)
#     else:
#         print("Invalid option. Please select 1 or 2.")
#
#
# if __name__ == "__main__":
#     main()


def playfair_cipher(text, key, mode='encrypt'):
    # Generate key matrix
    key = key.upper().replace('J', 'I')
    key_chars = []
    for c in key + 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if c.isalpha() and c not in key_chars and c != 'J':
            key_chars.append(c)

    matrix = [key_chars[i:i + 5] for i in range(0, 25, 5)]

    # Find position function
    def find_pos(char):
        for i in range(5):
            if char in matrix[i]:
                return i, matrix[i].index(char)

    # Prepare text
    text = text.upper().replace('J', 'I')
    text = ''.join(c for c in text if c.isalpha())

    if mode == 'encrypt':
        i = 0
        prepared = []
        while i < len(text):
            if i == len(text) - 1:
                prepared.extend([text[i], 'X'])
                break
            if text[i] == text[i + 1]:
                prepared.extend([text[i], 'X'])
                i += 1
            else:
                prepared.extend([text[i], text[i + 1]])
                i += 2
        text = ''.join(prepared)

    result = []
    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1] if i + 1 < len(text) else 'X'
        row_a, col_a = find_pos(a)
        row_b, col_b = find_pos(b)

        if row_a == row_b:  # Same row
            shift = 1 if mode == 'encrypt' else -1
            result.append(matrix[row_a][(col_a + shift) % 5])
            result.append(matrix[row_b][(col_b + shift) % 5])
        elif col_a == col_b:  # Same column
            shift = 1 if mode == 'encrypt' else -1
            result.append(matrix[(row_a + shift) % 5][col_a])
            result.append(matrix[(row_b + shift) % 5][col_b])
        else:  # Rectangle
            result.append(matrix[row_a][col_b])
            result.append(matrix[row_b][col_a])

    return ''.join(result)


if __name__ == "__main__":
    print("Enter the key for the Playfair Cipher:")
    key = input()

    print("Select an option:\n1. Encrypt\n2. Decrypt")
    choice = int(input())

    mode = 'encrypt' if choice == 1 else 'decrypt'
    operation = 'plaintext' if choice == 1 else 'ciphertext'

    print(f"Enter the {operation}:")
    text = input()

    result = playfair_cipher(text, key, mode)
    print(f"{'Cipher' if choice == 1 else 'Plain'}text:", result)
