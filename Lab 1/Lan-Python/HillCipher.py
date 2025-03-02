# def get_key_matrix(key):
#     key_matrix = [[0 for _ in range(3)] for _ in range(3)]
#     k = 0
#     for i in range(3):
#         for j in range(3):
#             key_matrix[i][j] = ord(key[k]) % 65
#             k += 1
#     return key_matrix
#
#
# def encrypt(key_matrix, message_vector):
#     cipher_matrix = [[0] for _ in range(3)]
#     for i in range(3):
#         for j in range(3):
#             cipher_matrix[i][0] += key_matrix[i][j] * message_vector[j][0]
#         cipher_matrix[i][0] = cipher_matrix[i][0] % 26
#     return cipher_matrix
#
#
# def hill_cipher(message, key):
#     key_matrix = get_key_matrix(key)
#
#     message_vector = [[0] for _ in range(3)]
#     for i in range(3):
#         message_vector[i][0] = ord(message[i]) % 65
#
#     cipher_matrix = encrypt(key_matrix, message_vector)
#
#     cipher_text = ""
#     for i in range(3):
#         cipher_text += chr(cipher_matrix[i][0] + 65)
#
#     return cipher_text
#
#
# def main():
#     message = input("Enter the message (3 characters): ").upper()
#     key = input("Enter the key (9 characters): ").upper()
#
#     cipher_text = hill_cipher(message, key)
#     print("Ciphertext:", cipher_text)
#
#
# if __name__ == "__main__":
#     main()


def hill_cipher(message, key):
    # Create key matrix (3x3)
    key_matrix = [[ord(key[3 * i + j]) % 65 for j in range(3)] for i in range(3)]

    # Create message vector (3x1)
    message_vector = [[ord(message[i]) % 65] for i in range(3)]

    # Encrypt
    cipher_matrix = [[0] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            cipher_matrix[i][0] += key_matrix[i][j] * message_vector[j][0]
        cipher_matrix[i][0] %= 26

    # Convert to text
    return ''.join(chr(cipher_matrix[i][0] + 65) for i in range(3))


if __name__ == "__main__":
    message = input("Enter the message (3 characters): ").upper()
    key = input("Enter the key (9 characters): ").upper()
    print("Ciphertext:", hill_cipher(message, key))
