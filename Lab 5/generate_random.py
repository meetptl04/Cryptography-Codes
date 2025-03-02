import random

# List of words to form random sentences
words = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
    "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
    "magna", "aliqua", "ut", "enim", "ad", "minim", "veniam", "quis", "nostrud",
    "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea", "commodo"
]

# Function to generate a random sentence
def generate_sentence():
    length = random.randint(6, 15)  # Random sentence length between 6 to 15 words
    sentence = ' '.join(random.choice(words) for _ in range(length)) + '.'
    return sentence.capitalize()

# Function to generate a random paragraph
def generate_paragraph():
    num_sentences = random.randint(5, 12)  # Random number of sentences per paragraph
    paragraph = ' '.join(generate_sentence() for _ in range(num_sentences))
    return paragraph

# Function to generate a random text file of a given size in bytes
def generate_text_file(file_name, size_in_bytes):
    text = ""
    while len(text.encode('utf-8')) < size_in_bytes:
        text += generate_paragraph() + "\n\n"  # Adding extra space between paragraphs

    # Write the generated text to a file ensuring the correct size
    with open(file_name, "w", encoding='utf-8') as file:
        file.write(text[:size_in_bytes])  # Make sure to slice the text to the exact byte size

    print(f"Generated file: {file_name} with size: {size_in_bytes} bytes")

# Automatically generate files of size 512 bytes, 1 KB, and 10 KB with readable text
generate_text_file("readable_512_bytes.txt", 512)
generate_text_file("readable_1kb.txt", 1024)
generate_text_file("readable_10kb.txt", 10240)

