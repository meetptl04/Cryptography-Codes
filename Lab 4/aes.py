class AES:
    # S-box lookup table
    S_BOX = [
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE,
        0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C,
        0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71,
        0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB,
        0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29,
        0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A,
        0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50,
        0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10,
        0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64,
        0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE,
        0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91,
        0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65,
        0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B,
        0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86,
        0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE,
        0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0,
        0x54, 0xBB, 0x16
    ]

    # Inverse S-box lookup table
    INV_S_BOX = [
        0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81,
        0xF3, 0xD7, 0xFB,
        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4,
        0xDE, 0xE9, 0xCB,
        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42,
        0xFA, 0xC3, 0x4E,
        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D,
        0x8B, 0xD1, 0x25,
        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D,
        0x65, 0xB6, 0x92,
        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7,
        0x8D, 0x9D, 0x84,
        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8,
        0xB3, 0x45, 0x06,
        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01,
        0x13, 0x8A, 0x6B,
        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0,
        0xB4, 0xE6, 0x73,
        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C,
        0x75, 0xDF, 0x6E,
        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA,
        0x18, 0xBE, 0x1B,
        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78,
        0xCD, 0x5A, 0xF4,
        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27,
        0x80, 0xEC, 0x5F,
        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93,
        0xC9, 0x9C, 0xEF,
        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83,
        0x53, 0x99, 0x61,
        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55,
        0x21, 0x0C, 0x7D
    ]

    # Round constant
    RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

    def __init__(self):
        self.key_schedule = None

    @staticmethod
    def galois_mult(a: int, b: int) -> int:
        """Helper method for Galois Field multiplication"""
        p = 0
        for _ in range(8):
            if b & 1:
                p ^= a
            hi_bit_set = a & 0x80
            a = (a << 1) & 0xFF
            if hi_bit_set:
                a ^= 0x1b
            b >>= 1
        return p

    def sub_bytes(self, state: bytearray) -> bytearray:
        """Apply S-box substitution to each byte in state"""
        for i in range(len(state)):
            state[i] = self.S_BOX[state[i]]
        return state

    def inv_sub_bytes(self, state: bytearray) -> bytearray:
        """Apply inverse S-box substitution to each byte in state"""
        for i in range(len(state)):
            state[i] = self.INV_S_BOX[state[i]]
        return state

    def shift_rows(self, state: bytearray) -> bytearray:
        """Shift rows of state array"""
        temp = bytearray(state)
        # Second row
        temp[1], temp[5], temp[9], temp[13] = state[5], state[9], state[13], state[1]
        # Third row
        temp[2], temp[6], temp[10], temp[14] = state[10], state[14], state[2], state[6]
        # Fourth row
        temp[3], temp[7], temp[11], temp[15] = state[15], state[3], state[7], state[11]
        return temp

    def inv_shift_rows(self, state: bytearray) -> bytearray:
        """Inverse shift rows of state array"""
        temp = bytearray(state)
        # Second row
        temp[5], temp[9], temp[13], temp[1] = state[1], state[5], state[9], state[13]
        # Third row
        temp[10], temp[14], temp[2], temp[6] = state[2], state[6], state[10], state[14]
        # Fourth row
        temp[15], temp[3], temp[7], temp[11] = state[3], state[7], state[11], state[15]
        return temp

    def mix_columns(self, state: bytearray) -> bytearray:
        """Mix columns transformation"""
        temp = bytearray(16)
        for i in range(4):
            s0 = state[i * 4]
            s1 = state[i * 4 + 1]
            s2 = state[i * 4 + 2]
            s3 = state[i * 4 + 3]

            temp[i * 4] = self.galois_mult(s0, 2) ^ self.galois_mult(s1, 3) ^ s2 ^ s3
            temp[i * 4 + 1] = s0 ^ self.galois_mult(s1, 2) ^ self.galois_mult(s2,
                                                                              3) ^ s3
            temp[i * 4 + 2] = s0 ^ s1 ^ self.galois_mult(s2, 2) ^ self.galois_mult(s3,
                                                                                   3)
            temp[i * 4 + 3] = self.galois_mult(s0, 3) ^ s1 ^ s2 ^ self.galois_mult(s3,
                                                                                   2)
        return temp

    def inv_mix_columns(self, state: bytearray) -> bytearray:
        """Inverse mix columns transformation"""
        temp = bytearray(16)
        for i in range(4):
            s0 = state[i * 4]
            s1 = state[i * 4 + 1]
            s2 = state[i * 4 + 2]
            s3 = state[i * 4 + 3]

            temp[i * 4] = (self.galois_mult(s0, 0x0e) ^ self.galois_mult(s1, 0x0b) ^
                           self.galois_mult(s2, 0x0d) ^ self.galois_mult(s3, 0x09))
            temp[i * 4 + 1] = (self.galois_mult(s0, 0x09) ^ self.galois_mult(s1, 0x0e) ^
                               self.galois_mult(s2, 0x0b) ^ self.galois_mult(s3, 0x0d))
            temp[i * 4 + 2] = (self.galois_mult(s0, 0x0d) ^ self.galois_mult(s1, 0x09) ^
                               self.galois_mult(s2, 0x0e) ^ self.galois_mult(s3, 0x0b))
            temp[i * 4 + 3] = (self.galois_mult(s0, 0x0b) ^ self.galois_mult(s1, 0x0d) ^
                               self.galois_mult(s2, 0x09) ^ self.galois_mult(s3, 0x0e))
        return temp

    def add_round_key(self, state: bytearray, round_key: bytes) -> None:
        """Add round key to state"""
        for i in range(16):
            state[i] ^= round_key[i]

    def generate_key_schedule(self, key: bytes) -> list:
        """Generate key schedule for all rounds"""
        w = [[0] * 4 for _ in range(44)]

        # First round key is the key itself
        for i in range(4):
            for j in range(4):
                w[i][j] = key[i * 4 + j]

        # Generate the rest of the round keys
        for i in range(4, 44):
            temp = w[i - 1].copy()

            if i % 4 == 0:
                # RotWord
                temp = temp[1:] + [temp[0]]

                # SubWord
                for j in range(4):
                    temp[j] = self.S_BOX[temp[j]]

                # XOR with RCON
                temp[0] ^= self.RCON[i // 4 - 1]

            for j in range(4):
                w[i][j] = w[i - 4][j] ^ temp[j]

        return w

    def get_round_key(self, round: int) -> bytes:
        """Get round key from key schedule"""
        round_key = bytearray(16)
        for i in range(4):
            for j in range(4):
                round_key[i * 4 + j] = self.key_schedule[round * 4 + i][j]
        return bytes(round_key)

    def encrypt(self, input_bytes: bytes, key: bytes) -> bytes:
        """Encrypt a 16-byte block using AES"""
        if len(input_bytes) != 16 or len(key) != 16:
            raise ValueError("Input and key must be 16 bytes")

        self.key_schedule = self.generate_key_schedule(key)
        state = bytearray(input_bytes)

        # Initial round
        self.add_round_key(state, self.get_round_key(0))

        # Main rounds
        for round in range(1, 10):
            state = self.sub_bytes(state)
            state = self.shift_rows(state)
            state = self.mix_columns(state)
            self.add_round_key(state, self.get_round_key(round))

        # Final round (no mixColumns)
        state = self.sub_bytes(state)
        state = self.shift_rows(state)
        self.add_round_key(state, self.get_round_key(10))

        return bytes(state)

    def decrypt(self, input_bytes: bytes, key: bytes) -> bytes:
        """Decrypt a 16-byte block using AES"""
        if len(input_bytes) != 16 or len(key) != 16:
            raise ValueError("Input and key must be 16 bytes")

        self.key_schedule = self.generate_key_schedule(key)
        state = bytearray(input_bytes)

        # Initial round
        self.add_round_key(state, self.get_round_key(10))
        state = self.inv_shift_rows(state)
        state = self.inv_sub_bytes(state)

        # Main rounds
        for round in range(9, 0, -1):
            self.add_round_key(state, self.get_round_key(round))
            state = self.inv_mix_columns(state)
            state = self.inv_shift_rows(state)
            state = self.inv_sub_bytes(state)

        # Final round
        self.add_round_key(state, self.get_round_key(0))

        return bytes(state)

    @staticmethod
    def hex_to_bytes(hex_str: str) -> bytes:
        """Convert hex string to bytes"""
        return bytes.fromhex(hex_str)

    @staticmethod
    def bytes_to_hex(data: bytes) -> str:
        """Convert bytes to hex string"""
        return data.hex()

#
# def main():
#     """Main method to test the implementation"""
#     try:
#         # Test vector
#         key_hex = "000102030405060708090a0b0c0d0e0f"
#         plaintext_hex = "00112233445566778899aabbccddeeff"
#
#         # Create AES instance
#         aes = AES()
#
#         # Convert hex strings to bytes
#         key = AES.hex_to_bytes(key_hex)
#         plaintext = AES.hex_to_bytes(plaintext_hex)
#
#         # Encrypt
#         print(f"Original plaintext: {AES.bytes_to_hex(plaintext)}")
#         ciphertext = aes.encrypt(plaintext, key)
#         print(f"Encrypted (hex): {AES.bytes_to_hex(ciphertext)}")
#
#         # Decrypt
#         decrypted = aes.decrypt(ciphertext, key)
#         print(f"Decrypted (hex): {AES.bytes_to_hex(decrypted)}")
#
#         # Verify
#         print(f"Decryption successful: {plaintext == decrypted}")
#
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         raise
#
#
# # if __name__ == "__main__":
# #     main()