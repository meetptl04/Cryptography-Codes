import random
import binascii

# Function to generate a random hexadecimal string of a given length in uppercase
def generate_hex_string(length):
    # Generate random bytes
    random_bytes = bytearray(random.getrandbits(8) for _ in range(length))
    # Convert the bytes to a hexadecimal string and convert it to uppercase
    hex_string = binascii.hexlify(random_bytes).decode('utf-8').upper()
    return hex_string

# Function to generate a random hexadecimal paragraph in uppercase
def generate_hex_paragraph():
    num_sentences = random.randint(5, 12)  # Random number of sentences per paragraph
    paragraph = ' '.join(generate_hex_string(random.randint(30, 60)) for _ in range(num_sentences))
    return paragraph

# Function to generate a random text file of a given size in bytes (in hexadecimal form, uppercase)
def generate_hex_file(file_name, size_in_bytes):
    hex_text = ""
    while len(hex_text.encode('utf-8')) < size_in_bytes:
        hex_text += generate_hex_paragraph() + "\n\n"  # Adding extra space between paragraphs

    # Write the generated hex text to a file ensuring the correct size
    with open(file_name, "w", encoding='utf-8') as file:
        file.write(hex_text[:size_in_bytes])  # Make sure to slice the text to the exact byte size

    print(f"Generated file: {file_name} with size: {size_in_bytes} bytes")

# Automatically generate files of size 512 bytes, 1 KB, and 10 KB with hexadecimal text in uppercase
generate_hex_file("hex_512_bytes.txt", 512)
generate_hex_file("hex_1kb.txt", 1024)
generate_hex_file("hex_10kb.txt", 10240)
