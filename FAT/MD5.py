import hashlib

def md5_encrypt(message):
    """
    Encrypts the input message using MD5 and returns the hash.
    """
    md5_hash = hashlib.md5(message.encode()).hexdigest()
    return md5_hash

def md5_check(message, md5_hash):
    """
    Checks if the MD5 hash of the input message matches the given hash.
    """
    return md5_encrypt(message) == md5_hash

# Example usage
message = 'Hello, World!'
encrypted_message = md5_encrypt(message)
print('Encrypted message (MD5):', encrypted_message)

# Verify if a message matches the hash
md5_hash = '65a8e27d8879283831b664bd8b7f0ad4'  # Example hash
is_match = md5_check(message, md5_hash)
print('Does the original message match the MD5 hash?', is_match)
