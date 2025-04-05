import random
import hashlib
from math import gcd


# Helper functions for display
def truncate(value, max_len=15):
    s = str(value)
    return f"{s[:max_len]}...({len(s) - max_len} digits)" if len(s) > max_len else s


def print_key(label, value):
    print(f"{label}: {truncate(value)}")


# Core DSS functions
def generate_primes(q_bits=160, p_bits=1024):
    """Generate DSA primes where q divides (p-1)"""
    while True:
        q = random.getrandbits(q_bits) | (1 << (q_bits - 1))
        if is_prime(q): break

    while True:
        k = random.getrandbits(p_bits - q_bits)
        p = q * k + 1
        if p.bit_length() == p_bits and is_prime(p):
            return p, q


def is_prime(n, trials=5):
    """Miller-Rabin primality test"""
    if n < 2: return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        if n % p == 0: return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(trials):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else:
            return False
    return True


def create_keys(p, q):
    """Generate DSA keys"""
    g = pow(random.randint(2, p - 2), (p - 1) // q, p)
    x = random.randint(1, q - 1)
    y = pow(g, x, p)
    return (p, q, g, y), x


def sign(message, priv_key, p, q, g):
    """Create DSA signature"""
    x = priv_key
    k = random.randint(1, q - 1)
    r = pow(g, k, p) % q
    h = int.from_bytes(hashlib.sha1(message).digest(), 'big')
    s = (pow(k, -1, q) * (h + x * r)) % q
    return (r, s)


def verify(message, sig, pub_key):
    """Verify DSA signature"""
    r, s = sig
    p, q, g, y = pub_key
    if not (0 < r < q and 0 < s < q): return False
    w = pow(s, -1, q)
    h = int.from_bytes(hashlib.sha1(message).digest(), 'big')
    u1 = (h * w) % q
    u2 = (r * w) % q
    v = (pow(g, u1, p) * pow(y, u2, p) % p) % q
    return v == r
