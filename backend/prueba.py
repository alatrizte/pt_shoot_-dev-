import hashlib
hashed = hashlib.sha3_256(b"1234Asdf").hexdigest()
print(hashed)