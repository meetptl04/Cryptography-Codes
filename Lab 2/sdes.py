class SimplifiedDES:
    def __init__(self, key=None):
        self.P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
        self.P8 = [6, 3, 7, 4, 8, 5, 10, 9]
        self.IP = [2, 6, 3, 1, 4, 8, 5, 7]
        self.EP = [4, 1, 2, 3, 2, 3, 4, 1]
        self.P4 = [2, 4, 3, 1]
        self.IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]
        self.S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
        self.S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]
        self.key = key if key else [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
        self.key1 = []
        self.key2 = []

    def set_key(self, key):
        if len(key) != 10:
            raise ValueError("Key must be a 10-bit binary list.")
        self.key = key

    def permute(self, bits, table):
        return [bits[i - 1] for i in table]

    def left_shift(self, bits, shifts):
        return bits[shifts:] + bits[:shifts]

    def key_generation(self):
        permuted_key = self.permute(self.key, self.P10)
        left, right = permuted_key[:5], permuted_key[5:]
        left, right = self.left_shift(left, 1), self.left_shift(right, 1)
        self.key1 = self.permute(left + right, self.P8)
        left, right = self.left_shift(left, 2), self.left_shift(right, 2)
        self.key2 = self.permute(left + right, self.P8)

    def xor(self, bits1, bits2):
        return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

    def sbox_substitution(self, bits, sbox):
        row = int(f"{bits[0]}{bits[3]}", 2)
        col = int(f"{bits[1]}{bits[2]}", 2)
        return [int(b) for b in f"{sbox[row][col]:02b}"]

    def fk(self, bits, key):
        left, right = bits[:4], bits[4:]
        expanded = self.permute(right, self.EP)
        xor_result = self.xor(expanded, key)
        left_sbox = self.sbox_substitution(xor_result[:4], self.S0)
        right_sbox = self.sbox_substitution(xor_result[4:], self.S1)
        sbox_result = left_sbox + right_sbox
        p4_result = self.permute(sbox_result, self.P4)
        return self.xor(left, p4_result) + right

    def encrypt(self, plaintext):
        initial_permutation = self.permute(plaintext, self.IP)
        round1 = self.fk(initial_permutation, self.key1)
        swapped = round1[4:] + round1[:4]
        round2 = self.fk(swapped, self.key2)
        return self.permute(round2, self.IP_inv)

    def decrypt(self, ciphertext):
        initial_permutation = self.permute(ciphertext, self.IP)
        round1 = self.fk(initial_permutation, self.key2)
        swapped = round1[4:] + round1[:4]
        round2 = self.fk(swapped, self.key1)
        return self.permute(round2, self.IP_inv)
