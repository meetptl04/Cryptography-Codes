import struct
from math import sin
from math import floor

def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

def md5(message):
    # Initialize variables
    a0 = 0x67452301
    b0 = 0xefcdab89
    c0 = 0x98badcfe
    d0 = 0x10325476

    # Pre-processing: adding a single 1 bit
    msg = bytearray(message)
    msg.append(0x80)

    # Pre-processing: padding with zeros
    while len(msg) % 64 != 56:
        msg.append(0)

    # Append original length in bits mod 2^64 to message
    msg += struct.pack('<Q', len(message) * 8)

    # Process the message in 16-word blocks
    for chunk_start in range(0, len(msg), 64):
        chunk = msg[chunk_start:chunk_start + 64]
        
        # Break chunk into sixteen 32-bit words
        M = [struct.unpack('<I', chunk[i:i+4])[0] for i in range(0, 64, 4)]

        # Initialize hash value for this chunk
        A, B, C, D = a0, b0, c0, d0

        # Main loop
        for i in range(64):
            if 0 <= i <= 15:
                F = (B & C) | ((~B) & D)
                g = i
            elif 16 <= i <= 31:
                F = (D & B) | ((~D) & C)
                g = (5*i + 1) % 16
            elif 32 <= i <= 47:
                F = B ^ C ^ D
                g = (3*i + 5) % 16
            elif 48 <= i <= 63:
                F = C ^ (B | (~D))
                g = (7*i) % 16

            F = (F + A + M[g] + int(4294967296 * abs(sin(i + 1)))) & 0xFFFFFFFF
            A = D
            D = C
            C = B
            B = (B + left_rotate(F, [7, 12, 17, 22][i//16])) & 0xFFFFFFFF

        # Add this chunk's hash to result so far
        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF

    # Produce the final hash value
    return struct.pack('<IIII', a0, b0, c0, d0).hex()

def md5_hash(message):
    return md5(message.encode())
