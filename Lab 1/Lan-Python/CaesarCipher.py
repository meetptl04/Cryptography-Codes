# def encrypt(text, shift):
#     result = ""
#     for char in text:
#         if char.isalpha():
#             # Determine if the character is uppercase or lowercase
#             base = ord('a') if char.islower() else ord('A')
#             # Apply the Caesar cipher formula
#             result += chr((ord(char) - base + shift) % 26 + base)
#         else:
#             # Keep non-alphabetic characters unchanged
#             result += char
#     return result
#
#
# def decrypt(cipher, shift):
#     result = ""
#     for char in cipher:
#         if char.isalpha():
#             # Determine if the character is uppercase or lowercase
#             base = ord('a') if char.islower() else ord('A')
#             # Apply the reverse Caesar cipher formula
#             result += chr((ord(char) - base - shift + 26) % 26 + base)
#         else:
#             # Keep non-alphabetic characters unchanged
#             result += char
#     return result
#
#
# def main():
#     shift = 3
#
#     print("Select an option:")
#     print("1. Encrypt a message")
#     print("2. Decrypt a message")
#
#     try:
#         choice = int(input())
#
#         if choice == 1:
#             print("Enter the text to be encrypted:")
#             text = input()
#             encrypted = encrypt(text, shift)
#             print("Encrypted Text:", encrypted)
#         elif choice == 2:
#             print("Enter the text to be decrypted:")
#             cipher = input()
#             decrypted = decrypt(cipher, shift)
#             print("Decrypted Text:", decrypted)
#         else:
#             print("Invalid option. Please select 1 or 2.")
#     except ValueError:
#         print("Please enter a valid number.")
#
#
# if __name__ == "__main__":
#     main()


def caesar(text, shift, mode='encrypt'):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            # If decrypting, reverse the shift
            s = shift if mode == 'encrypt' else -shift
            result += chr((ord(char) - base + s) % 26 + base)
        else:
            result += char
    return result


if __name__ == "__main__":
    shift = 3

    print("Select an option:\n1. Encrypt a message\n2. Decrypt a message")
    choice = int(input())

    if choice in [1, 2]:
        mode = 'encrypt' if choice == 1 else 'decrypt'
        text = input(f"Enter the text to be {mode}ed:\n")
        result = caesar(text, shift, mode)
        print(f"{mode.capitalize()}ed Text:", result)
    else:
        print("Invalid option. Please select 1 or 2.")
