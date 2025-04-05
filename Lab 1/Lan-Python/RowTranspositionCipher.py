# def row_transposition(text, key, decrypt=False):
#     columns = len(key)
#     rows = (len(text) + columns - 1) // columns  # Ceiling division
#
#     if not decrypt:  # Encrypt
#         # Pad the plaintext if needed
#         padded_text = text + 'X' * (rows * columns - len(text))
#
#         # Fill the grid row by row
#         grid = [['' for _ in range(columns)] for _ in range(rows)]
#         for i in range(len(padded_text)):
#             grid[i // columns][i % columns] = padded_text[i]
#
#         # Read off by columns according to key
#         result = ''
#         for k in key:
#             col = int(k)
#             for row in range(rows):
#                 result += grid[row][col]
#
#         return result
#
#     else:  # Decrypt
#         # Create empty grid
#         grid = [['' for _ in range(columns)] for _ in range(rows)]
#
#         # Fill the grid column by column according to key
#         index = 0
#         for k in key:
#             col = int(k)
#             for row in range(rows):
#                 if index < len(text):
#                     grid[row][col] = text[index]
#                     index += 1
#
#         # Read off row by row
#         result = ''
#         for row in grid:
#             result += ''.join(row)
#
#         # Remove padding if any
#         return result.replace('X', '')
#
#
# if __name__ == "__main__":
#     print("Row Transposition Cipher")
#     print("Choose an option:")
#     print("1. Encrypt")
#     print("2. Decrypt")
#     choice = int(input())
#
#     key = input("Enter the key (numeric string): ")
#
#     if choice == 1:
#         plaintext = input("Enter the plaintext: ")
#         ciphertext = row_transposition(plaintext, key)
#         print("Encrypted text:", ciphertext)
#     elif choice == 2:
#         ciphertext = input("Enter the ciphertext: ")
#         plaintext = row_transposition(ciphertext, key, decrypt=True)
#         print("Decrypted text:", plaintext)
#     else:
#         print("Invalid choice.")


def row_transposition(text, key, decrypt=False):
    columns = len(key)
    rows = (len(text) + columns - 1) // columns

    if not decrypt:  # Encrypt
        # Pad text and create grid
        text = text.ljust(rows * columns, 'X')
        grid = [text[i:i + columns] for i in range(0, len(text), columns)]
        # Read off by columns according to key
        return ''.join(grid[r][int(k)] for k in key for r in range(rows))
    else:  # Decrypt
        # Create empty grid
        grid = [['' for _ in range(columns)] for _ in range(rows)]
        # Fill grid by columns according to key
        index = 0
        for k in key:
            col = int(k)
            for row in range(rows):
                if index < len(text):
                    grid[row][col] = text[index]
                    index += 1
        # Read grid row by row and remove padding
        return ''.join(''.join(row) for row in grid).rstrip('X')


if __name__ == "__main__":
    choice = int(input("1. Encrypt\n2. Decrypt\nChoice: "))
    key = input("Key (numeric): ")
    text = input("Text: ")

    result = row_transposition(text, key, choice == 2)
    print(f"Result: {result}")


