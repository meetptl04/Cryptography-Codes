from Crypto.Cipher import DES

# Get general help on the DES module
help(DES)

# For more specific information on creating a new DES object
help(DES.new)

# Create a DES object (you need a key for this)
des = DES.new(b'01234567', DES.MODE_ECB)

# Get help on the encrypt method
help(des.encrypt)

# Get help on the decrypt method
help(des.decrypt)
