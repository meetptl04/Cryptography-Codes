import random
import math

# A set will be the collection of prime numbers
# where we can select random primes p and q
prime_numbers = set()
public_key = None
private_key = None
n = None


def get_keys():
    """Returns the public key and n."""
    print(f"Public Key (e): {public_key}")
    print(f"n: {n}")
    return public_key, n


def fill_prime_numbers():
    """Fills the prime number set using Sieve of Eratosthenes."""
    sieve = [True] * 250
    sieve[0] = sieve[1] = False

    for i in range(2, 250):
        if sieve[i]:
            for j in range(i * 2, 250, i):
                sieve[j] = False

    # Adding prime numbers to the set
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
    """Generates public and private keys."""
    global public_key, private_key, n

    prime1 = pick_random_prime()
    prime2 = pick_random_prime()
    
    n = prime1 * prime2
    fi = (prime1 - 1) * (prime2 - 1)
    
    e = 2
    while math.gcd(e, fi) != 1:
        e += 1

    public_key = e
    
    # Find private key d
    d = 2
    while (d * e) % fi != 1:
        d += 1

    private_key = d

    # Print out the details for the server (private key and n)
    print(f"Private Key (d): {private_key}")
    print(f"Prime1: {prime1}")
    print(f"Prime2: {prime2}")
    print(f"Public Key (e): {public_key}")
    print(f"n: {n}")
    print(f"Euler's Totient (fi): {fi}")


def encrypt(message, public_key, n):
    """Encrypts the message using the public key."""
    e = public_key
    encrypted_text = 1
    while e > 0:
        encrypted_text *= message
        encrypted_text %= n
        e -= 1
    return encrypted_text


def decrypt(encrypted_text):
    """Decrypts the message using the private key."""
    global private_key, n
    d = private_key
    decrypted = 1
    while d > 0:
        decrypted *= encrypted_text
        decrypted %= n
        d -= 1
    return decrypted


def encoder(message, num1, num2):
    """Encodes the message to encrypted form using the public key."""
    print("Encoding message...")
    encoded = [encrypt(ord(letter), num1, num2) for letter in message]
    print(f"Encoded message: {encoded}")
    return encoded


def decoder(encoded):
    """Decodes the message back to plaintext using the private key."""
    print("Decoding message...")
    decoded_message = ''.join(chr(decrypt(num)) for num in encoded)
    print(f"Decoded message: {decoded_message}")
    return decoded_message

