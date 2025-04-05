import random
import hashlib
import math

def is_prime(n, k=5):
    """Miller-Rabin primality test."""
    if n <= 1:
        return False
    elif n <= 3:
        return True
    # Write n-1 as d*2^s
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1
    # Witness loop
    for _ in range(k):
        a = random.randint(2, min(n-2, 1 << 20))
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s-1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits=16):
    """Generate a random prime number."""
    while True:
        p = random.getrandbits(bits)
        p |= (1 << (bits - 1)) | 1
        if is_prime(p):
            return p

def prime_factors(n):
    """Return prime factors of n."""
    factors = set()
    while n % 2 == 0:
        factors.add(2)
        n //= 2
    i = 3
    while i*i <= n:
        while n % i == 0:
            factors.add(i)
            n //= i
        i += 2
    if n > 2:
        factors.add(n)
    return factors

def find_generator(p):
    """Find a primitive root modulo p."""
    if p == 2:
        return 1
    factors = prime_factors(p-1)
    for g in range(2, p):
        if pow(g, p-1, p) != 1:
            continue
        if all(pow(g, (p-1)//f, p) != 1 for f in factors):
            return g
    raise ValueError("No generator found")

def generate_keys(bits=16):
    """Generate ElGamal keys."""
    p = generate_prime(bits)
    g = find_generator(p)
    x = random.randint(1, p-2)
    h = pow(g, x, p)
    return (p, g, h), x

def secure_hash(message, mod):
    """Compute SHA-512 hash modulo."""
    hash_obj = hashlib.sha512(message if isinstance(message, bytes) else message.encode())
    hash_bytes = hash_obj.digest()
    print("SHA512:", hash_obj.hexdigest())
    return int.from_bytes(hash_bytes, "big") % mod

def sign(message, private_key, p, g):
    """Sign message with ElGamal."""
    x = private_key
    k = random.randint(2, p-2)
    while math.gcd(k, p-1) != 1:
        k = random.randint(2, p-2)
    r = pow(g, k, p)
    hash_val = secure_hash(message, p-1)
    s = ((hash_val - x * r) * pow(k, -1, p-1)) % (p-1)
    return (r, s)

def verify(message, signature, public_key):
    """Verify ElGamal signature."""
    r, s = signature
    p, g, h = public_key
    hash_val = secure_hash(message, p-1)
    left = pow(g, hash_val, p)
    right = (pow(h, r, p) * pow(r, s, p)) % p
    return left == right
