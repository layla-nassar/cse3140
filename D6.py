from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import unpad
import os

private_key = """-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCMqf4MyQYxZ5wxuYbFtztnRdeY4mVfgzFUs2/9i4nUJvlltSdD
7NApUynU+5UeyLo+kUpxpWSvFc2H+3RDHrNVqxDsDKqeoh2giLPQP1bh+oiBQM3e
EQiEOHC+OW3fFNIe47EB4j0sEtK+vlrR0BGqIwHOgabaFqJATO+K+QSJ8wIDAQAB
AoGACaCa5DogA+KhBKA7kq2zUaKsmmioYoyipDbxy8swoEYYnLb03IfJSYLJIqwj
bSt039Jm43db+EXIPu3da7iesnzWxTjg7TGp7SnqpUoxDDK5YwtppMwJ7imWRae7
O/iQl5VSJ6TqsLCKLScpK/zVuZli4RM6mqb8ihl99mX61AECQQC2DoZ3C8vmCP6X
4P1iEGsqlEw5Ul9/EKlpgkLjsiwh+W4o6IgO/YUc/Efph5rqQYc2k6dKeysV7o+g
8bJzmbXzAkEAxcuhyamMeRH9EP6zbTGNoDx5eI+2+enNpu1iMbKy0UFpFGb/XxYg
K3cc83RhKOPUjmdzB9GLPdDgwP2m/DrcAQJAXOhavMP7YUBz1MRP6sygNBGMOLCN
5YV2P07nndWeahQloKDSVnwQg3NHq6i1aRjZzQNbG0px+XZOO/88Z3wo+wJBAIyd
cpxKI+piZnWxjN9g7h1vQK/8A4nxtFkqw7cvIj7vcIOnoX743M/pszRElVobdh3y
3208g+/jUhUBfrgsJAECQGen1/b33n45h3mv7GKCDm9mIOQ2BSv1yPh1X0dPpjjR
s+unpawHxTZA8NiB60++Qnx7NYPNe5FEy8m0DX+bpVc=
-----END RSA PRIVATE KEY-----"""

# Input encrypted shared key filename (EncryptedSharedKey)
encrypted_shared = input("Enter the encrypted shared key filename (e.g., EncryptedSharedKey): ")
encrypted_shared_key = "/home/cse/Lab3/Solutions/" + encrypted_shared

# Output file where decrypted key will be saved
decrypted_shared_key_file = "/home/cse/Lab3/Solutions/DecryptedSharedKey"

# Read the encrypted shared key
with open(encrypted_shared_key, "rb") as f:
    encrypted_message = f.read()

# Load the private key and initialize RSA decryption
rsa_key = RSA.import_key(private_key)
cipher_rsa = PKCS1_OAEP.new(rsa_key)

# Decrypt the shared key
try:
    decrypted_shared_key = cipher_rsa.decrypt(encrypted_message)
except ValueError as e:
    print(f"Error during decryption: {e}")
else:
    # Write the decrypted key (as bytes, not as a string)
    with open(decrypted_shared_key_file, "wb") as f:
        f.write(decrypted_shared_key)
    print("Decryption successful. Shared key saved to:", decrypted_shared_key_file)

# Now you can decrypt the encrypted files using the decrypted AES shared key.
def decrypt_file(filepath, shared_key):
    # Initialize AES in CBC mode with the decrypted shared key
    cipher_aes = AES.new(shared_key, AES.MODE_CBC)

    # Read the file content (including the IV)
    with open(filepath, "rb") as f:
        iv = f.read(16)  # The first 16 bytes are the IV
        encrypted_data = f.read()

    # Decrypt the data
    decrypted_data = unpad(cipher_aes.decrypt(encrypted_data), AES.block_size)

    # Write the decrypted data back to the file (or another file if needed)
    with open(filepath.replace(".encrypted", ""), "wb") as f:
        f.write(decrypted_data)

# Decrypt all encrypted files in the directory
def attack_directory(attacking_directory):
    # Read the decrypted shared key
    with open(decrypted_shared_key_file, "rb") as f:
        shared_key = f.read()

    for file in os.listdir(attacking_directory):
        filepath = os.path.join(attacking_directory, file)
        if filepath.endswith(".encrypted"):
            print(f"Decrypting: {filepath}")
            decrypt_file(filepath, shared_key)

# Start decrypting
attack_directory("/home/cse/Lab3/Solutions/")
