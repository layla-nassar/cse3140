import os
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15


# Define paths
lab3_path = "/home/cse/Lab3"
q3_pubkey_file = os.path.join(lab3_path, "Q3pk.pem")
q3_files_path = os.path.join(lab3_path, "Q3files")


# Load public key
with open(q3_pubkey_file, "rb") as f:
   public_key = RSA.import_key(f.read())


# Check each .exe file
for filename in os.listdir(q3_files_path):
   if filename.endswith(".exe"):
       exe_file = os.path.join(q3_files_path, filename)
       sign_file = exe_file + ".sign"  # Corresponding .sign file


       # Skip if signature file is missing
       if not os.path.exists(sign_file):
           continue
      
       # Compute SHA-256 hash of the executable
       with open(exe_file, "rb") as f:
           file_data = f.read()
           file_hash = SHA256.new(file_data)


       # Read the signature
       with open(sign_file, "rb") as f:
           signature = f.read()


       # Verify the signature
       try:
           pkcs1_15.new(public_key).verify(file_hash, signature)
           print(f"Correctly signed file: {filename}")
           break  # Stop once we find the correctly signed file
       except (ValueError, TypeError):
           pass  # Ignore invalid signatures
