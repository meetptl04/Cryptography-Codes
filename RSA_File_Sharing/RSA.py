import random
import math
import hashlib

# Global variables for key parameters.
prime_numbers = set()
public_key = None
private_key = None
n = None

def get_keys():
    """Returns the public key and modulus n."""
    print(f"Public Key (e): {public_key}")
    print(f"n: {n}")
    return public_key, n

def fill_prime_numbers():
    """Fills the prime number set using the Sieve of Eratosthenes."""
    sieve = [True] * 250
    sieve[0] = sieve[1] = False
    for i in range(2, 250):
        if sieve[i]:
            for j in range(i * 2, 250, i):
                sieve[j] = False
    # Add primes to the set.
    for i in range(len(sieve)):
        if sieve[i]:
            prime_numbers.add(i)

def pick_random_prime():
    """Picks a random prime from the prime number set."""
    global prime_numbers
    prime_list = list(prime_numbers)
    random_prime = random.choice(prime_list)
    prime_numbers.remove(random_prime)
    return random_prime

def set_keys():
    """Generates public and private keys using two randomly picked primes."""
    global public_key, private_key, n
    prime1 = pick_random_prime()
    prime2 = pick_random_prime()
    n = prime1 * prime2
    fi = (prime1 - 1) * (prime2 - 1)
    e = 2
    while math.gcd(e, fi) != 1:
        e += 1
    public_key = e
    # Find the private key d (modular inverse).
    d = 2
    while (d * e) % fi != 1:
        d += 1
    private_key = d
    print(f"Private Key (d): {private_key}")
    print(f"Prime1: {prime1}")
    print(f"Prime2: {prime2}")
    print(f"Public Key (e): {public_key}")
    print(f"n: {n}")
    print(f"Euler's Totient (fi): {fi}")

def secure_hash(message, mod):
    """
    Computes the SHA-512 digest of the message.
    Prints the full SHA-512 hash (in hex).
    Converts the digest to an integer and reduces it modulo mod.
    """
    if isinstance(message, bytes):
        data = message
    else:
        data = message.encode("utf-8")
    hash_obj = hashlib.sha512(data)
    hash_hex = hash_obj.hexdigest()
    print("Full SHA512 Hash:", hash_hex)
    hash_bytes = hash_obj.digest()
    hash_value = int.from_bytes(hash_bytes, byteorder="big")
    return hash_value % mod

def sign(message):
    """
    Signs the message using the private key.
    Computes digest = SHA512(message) mod n, prints it, and then
    returns signature = digest^d mod n.
    """
    global private_key, n
    hash_val = secure_hash(message, n)
    print("Computed SHA512 digest (mod n) for signing:", hash_val)
    signed = pow(hash_val, private_key, n)
    return signed

def verify(signed_message, message, pub_key, mod):
    """
    Verifies the signature using the provided public key.
    Computes digest = SHA512(message) mod mod and prints it.
    Also prints the recovered hash from the signature.
    Returns True if they match.
    """
    hash_val = secure_hash(message, mod)
    print("Computed SHA512 digest (mod n) for verification:", hash_val)
    recovered = pow(signed_message, pub_key, mod)
    print("Recovered hash from signature:", recovered)
    return recovered == hash_val

def encrypt(message, pub_key, mod):
    """Encrypts the message using the public key (not used in our signature demo)."""
    e = pub_key
    encrypted_text = 1
    while e > 0:
        encrypted_text *= message
        encrypted_text %= mod
        e -= 1
    return encrypted_text

def decrypt(encrypted_text):
    """Decrypts the message using the private key (not used in our signature demo)."""
    global private_key, n
    d = private_key
    decrypted = 1
    while d > 0:
        decrypted *= encrypted_text
        decrypted %= n
        d -= 1
    return decrypted

def encoder(message, num1, num2):
    """Encodes the message using the public key."""
    print("Encoding message...")
    encoded = [encrypt(ord(letter), num1, num2) for letter in message]
    print(f"Encoded message: {encoded}")
    return encoded

def decoder(encoded):
    """Decodes the message using the private key."""
    print("Decoding message...")
    decoded_message = ''.join(chr(decrypt(num)) for num in encoded)
    print(f"Decoded message: {decoded_message}")
    return decoded_message
