import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Hash import MD5




with open(os.path.join("/home/cse/Lab3/Q5files", "Encrypted5"), 'rb') as f:
    iv = f.read(16)
    ciphertext = f.read()
h = MD5.new()
with open(os.path.join("/home/cse/Lab3/Q5files", "R5.py"), 'rb') as afile:
    buf = afile.read(128)
    while len(buf) > 0:
        h.update(buf)
        buf = afile.read(128)
key = h.digest()
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
with open('Q5a', 'a') as f:
    f.write(plaintext.decode())
