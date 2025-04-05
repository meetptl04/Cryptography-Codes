import hashlib

message = input("Enter the message : ")

encrypted_msg = hashlib.md5(message.encode()).hexdigest()

print(f"encrypted_msg : {encrypted_msg}")