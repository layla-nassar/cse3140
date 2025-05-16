from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Private RSA key for decryption
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

# Input encrypted shared key filename
encrypted_shared = input("Enter the encrypted shared key filename: ")
encrypted_shared_key = "/home/cse/Lab3/Solutions/" + encrypted_shared

# Output file where decrypted key will be saved
decrypted_shared_key_file = "/home/cse/Lab3/Solutions/DecryptedSharedKey"

# Decrypt the shared key
with open(encrypted_shared_key, "rb") as c:
    encrypted_message = c.read()  # Read the encrypted shared key

# Load the private key and initialize RSA decryption
rsa_key = RSA.import_key(private_key)
cipher_rsa = PKCS1_OAEP.new(rsa_key)

# Decrypt the encrypted shared key
try:
    decrypted_message = cipher_rsa.decrypt(encrypted_message)
except ValueError as e:
    print(f"Error during decryption: {e}")
else:
    # Write the decrypted key (as bytes, not as a string)
    with open(decrypted_shared_key_file, "wb") as f:
        f.write(decrypted_message)
    print("Decryption successful. Shared key saved to:", decrypted_shared_key_file)
