# def encrypt(plaintext, key):
#     ciphertext = ""
#     key_index = 0
#
#     for i in range(len(plaintext)):
#         plaintext_char = plaintext[i]
#         if plaintext_char.isalpha():
#             key_char = key[key_index % len(key)]
#             shift = ord(key_char.upper()) - ord('A')
#
#             if plaintext_char.isupper():
#                 encrypted_char = chr(
#                     ((ord(plaintext_char) - ord('A') + shift) % 26) + ord('A'))
#                 ciphertext += encrypted_char
#             else:
#                 encrypted_char = chr(
#                     ((ord(plaintext_char) - ord('a') + shift) % 26) + ord('a'))
#                 ciphertext += encrypted_char
#             key_index += 1
#         else:
#             ciphertext += plaintext_char
#
#     return ciphertext
#
#
# def decrypt(ciphertext, key):
#     plaintext = ""
#     key_index = 0
#
#     for i in range(len(ciphertext)):
#         ciphertext_char = ciphertext[i]
#         if ciphertext_char.isalpha():
#             key_char = key[key_index % len(key)]
#             shift = ord(key_char.upper()) - ord('A')
#
#             if ciphertext_char.isupper():
#                 decrypted_char = chr(
#                     ((ord(ciphertext_char) - ord('A') - shift + 26) % 26) + ord('A'))
#                 plaintext += decrypted_char
#             else:
#                 decrypted_char = chr(
#                     ((ord(ciphertext_char) - ord('a') - shift + 26) % 26) + ord('a'))
#                 plaintext += decrypted_char
#             key_index += 1
#         else:
#             plaintext += ciphertext_char
#
#     return plaintext
#
#
# def main():
#     print("Vigenère Cipher")
#     print("Choose an option:")
#     print("1. Encrypt")
#     print("2. Decrypt")
#     choice = int(input())
#
#     key = input("Enter the key: ")
#
#     if choice == 1:
#         plaintext = input("Enter the plaintext: ")
#         ciphertext = encrypt(plaintext, key)
#         print("Encrypted text:", ciphertext)
#     elif choice == 2:
#         ciphertext = input("Enter the ciphertext: ")
#         decrypted_text = decrypt(ciphertext, key)
#         print("Decrypted text:", decrypted_text)
#     else:
#         print("Invalid choice.")
#
#
# if __name__ == "__main__":
#     main()


def vigenere(text, key, decrypt=False):
    result = ""
    key_idx = 0

    for char in text:
        if char.isalpha():
            # Get shift from key
            shift = ord(key[key_idx % len(key)].upper()) - ord('A')
            if decrypt:
                shift = -shift

            # Apply shift based on case
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
            key_idx += 1
        else:
            result += char

    return result


if __name__ == "__main__":
    print("Vigenère Cipher")
    choice = int(input("1. Encrypt\n2. Decrypt\nChoice: "))
    key = input("Key: ")

    if choice in [1, 2]:
        text = input(f"{'Plain' if choice == 1 else 'Cipher'}text: ")
        result = vigenere(text, key, choice == 2)
        print(f"{'Encrypted' if choice == 1 else 'Decrypted'} text: {result}")
    else:
        print("Invalid choice.")
