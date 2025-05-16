import hashlib
import os


# Define file paths
lab3_path = "/home/cse/Lab3"
q2_hash_file = os.path.join(lab3_path, "Q2hash.txt")
q2_files_path = os.path.join(lab3_path, "Q2files")


# Read the expected hash from Q2hash.txt
with open(q2_hash_file, "r") as f:
   expected_hash = f.read().strip()


def compute_sha256(file_path):
   """Compute the SHA-256 hash of a file."""
   sha256 = hashlib.sha256()
   with open(file_path, "rb") as f:
       while chunk := f.read(4096):  # Read in chunks to handle large files
           sha256.update(chunk)
   return sha256.hexdigest()


# Find the matching file
matching_files = []
for filename in os.listdir(q2_files_path):
   file_path = os.path.join(q2_files_path, filename)
  
   if os.path.isfile(file_path):  # Only process files, not directories
       file_hash = compute_sha256(file_path)
       if file_hash == expected_hash:
           matching_files.append(filename)


# Output the result
if matching_files:
   print(f"Matching file(s): {', '.join(matching_files)}")
else:
   print("No matching file found.")


import hashlib
import os


# Define file paths
lab3_path = "/home/cse/Lab3"
q2_hash_file = os.path.join(lab3_path, "Q2hash.txt")
q2_files_path = os.path.join(lab3_path, "Q2files")


# Read the expected hash from Q2hash.txt
with open(q2_hash_file, "r") as f:
   expected_hash = f.read().strip()


def compute_sha256(file_path):
   """Compute the SHA-256 hash of a file."""
   sha256 = hashlib.sha256()
   with open(file_path, "rb") as f:
       while chunk := f.read(4096):  # Read in chunks to handle large files
           sha256.update(chunk)
   return sha256.hexdigest()


# Find the matching file
matching_files = []
for filename in os.listdir(q2_files_path):
   file_path = os.path.join(q2_files_path, filename)
  
   if os.path.isfile(file_path):  # Only process files, not directories
       file_hash = compute_sha256(file_path)
       if file_hash == expected_hash:
           matching_files.append(filename)


# Output the result
if matching_files:
   print(f"Matching file(s): {', '.join(matching_files)}")
else:
   print("No matching file found.")


