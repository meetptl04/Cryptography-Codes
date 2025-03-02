# def rail_fence_cipher(text, rails, mode='encrypt'):
#     # Create the rail fence pattern
#     fence = [['\n' for _ in range(len(text))] for _ in range(rails)]
#
#     # Mark the rail pattern with placeholders
#     row, down = 0, True
#     for i in range(len(text)):
#         fence[row][i] = '*' if mode == 'decrypt' else text[i]
#         if row == 0:
#             down = True
#         if row == rails - 1:
#             down = False
#         row = row + 1 if down else row - 1
#
#     if mode == 'encrypt':
#         # Read off the fence
#         result = ''.join(char for rail in fence for char in rail if char != '\n')
#     else:  # decrypt
#         # Fill the fence with ciphertext
#         index = 0
#         for i in range(rails):
#             for j in range(len(text)):
#                 if fence[i][j] == '*':
#                     fence[i][j] = text[index]
#                     index += 1
#
#         # Read off in zigzag pattern
#         result = ''
#         row, down = 0, True
#         for i in range(len(text)):
#             result += fence[row][i]
#             if row == 0:
#                 down = True
#             if row == rails - 1:
#                 down = False
#             row = row + 1 if down else row - 1
#
#     return result
#
#
# if __name__ == "__main__":
#     print("Rail Fence Cipher")
#     print("Choose an option:")
#     print("1. Encrypt")
#     print("2. Decrypt")
#     choice = int(input())
#
#     rails = int(input("Enter the number of rails: "))
#
#     if choice == 1:
#         plaintext = input("Enter the plaintext: ")
#         ciphertext = rail_fence_cipher(plaintext, rails, 'encrypt')
#         print("Encrypted text:", ciphertext)
#     elif choice == 2:
#         ciphertext = input("Enter the ciphertext: ")
#         plaintext = rail_fence_cipher(ciphertext, rails, 'decrypt')
#         print("Decrypted text:", plaintext)
#     else:
#         print("Invalid choice.")


def rail_fence(text, rails, decrypt=False):
    # Create zigzag pattern indices
    pattern = []
    r, step = 0, 1
    for i in range(len(text)):
        pattern.append(r)
        r += step
        if r == 0 or r == rails - 1:
            step = -step

    if decrypt:
        # For decryption
        result = [''] * len(text)
        index = 0
        # Read off in rail order
        for r in range(rails):
            for i, pos in enumerate(pattern):
                if pos == r:
                    result[i] = text[index]
                    index += 1
        return ''.join(result)
    else:
        # For encryption
        fence = [[] for _ in range(rails)]
        for i, char in enumerate(text):
            fence[pattern[i]].append(char)
        return ''.join(sum(fence, []))  # Flatten the fence


if __name__ == "__main__":
    choice = int(input("1. Encrypt\n2. Decrypt\nChoice: "))
    rails = int(input("Rails: "))
    text = input("Text: ")

    result = rail_fence(text, rails, choice == 2)
    print(f"{'Decrypted' if choice == 2 else 'Encrypted'} text:", result)
