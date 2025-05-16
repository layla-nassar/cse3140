import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

with open(os.path.join("/home/cse/Lab3/Q4files", "Encrypted4"), 'rb') as f:
   iv = f.read(16)
   ciphertext = f.read()

key = b'\x8a\xf0q7c\xa9yq\xfdJ\x885\xb0|t\x15'
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

# Fix: Use "w" instead of "a" to avoid duplicate entries
with open('Q4a', 'w') as f:
   f.write(plaintext.decode())

print("Decryption successful! Check Q4a for the output.")
