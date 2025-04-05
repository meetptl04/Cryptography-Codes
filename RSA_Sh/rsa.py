import random
import math
import hashlib

prime_set = set()
public_exp = None
private_exp = None
modulus = None

def show_keys():
    print(f"Public Exponent (e): {public_exp}")
    print(f"Modulus Value (n): {modulus}")
    return public_exp, modulus

def populate_primes():
    sieve = [True] * 250
    sieve[0] = sieve[1] = False
    for i in range(2, 250):
        if sieve[i]:
            for j in range(i*2, 250, i):
                sieve[j] = False
    for i in range(len(sieve)):
        if sieve[i]:
            prime_set.add(i)

def get_prime():
    prime = random.choice(list(prime_set))
    prime_set.remove(prime)
    return prime

def generate_rsa_keys():
    global public_exp, private_exp, modulus
    p = get_prime()
    q = get_prime()
    modulus = p * q
    phi = (p-1) * (q-1)
    
    public_exp = 2
    while math.gcd(public_exp, phi) != 1:
        public_exp += 1
    
    private_exp = 1
    while (private_exp * public_exp) % phi != 1:
        private_exp += 1
    
    print("\n--- RSA Key Details ---")
    print(f"Prime 1: {p}")
    print(f"Prime 2: {q}")
    print(f"Public Key (e): {public_exp}")
    print(f"Private Key (d): {private_exp}")
    print(f"Modulus (n): {modulus}")
    print(f"Euler Totient (φ): {phi}\n")

def hash_data(data, mod):
    if isinstance(data, str):
        data = data.encode()
    hash_obj = hashlib.sha512(data)
    full_hash = hash_obj.hexdigest()
    print(f"Full SHA-512 Hash:\n{full_hash}")
    return int.from_bytes(hash_obj.digest(), 'big') % mod

def create_signature(message):
    hash_value = hash_data(message, modulus)
    print(f"Hash Value for Signing: {hash_value}")
    return pow(hash_value, private_exp, modulus)

def verify_signature(signature, message, e, n):
    hash_value = hash_data(message, n)
    print(f"Verification Hash Value: {hash_value}")
    recovered = pow(signature, e, n)
    print(f"Recovered Signature Value: {recovered}")
    return recovered == hash_value
