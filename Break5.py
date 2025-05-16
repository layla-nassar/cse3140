import hashlib
import subprocess
import time
import sys
from itertools import product


start = time.time()
print("Start time: 0 seconds")


gang_file_path = "/home/cse/Lab1/Q5/gang"
hashed_pw_file_path = "/home/cse/Lab1/Q5/HashedPWs"
pwned_pw_file_path = "/home/cse/Lab1/Q5/PwnedPWs100k"
login_script_path = "/home/cse/Lab1/Q5/Login.pyc"


exposed_users = {"SkyRedFalcon914", "MountainPurpleShark585", "ForestGreenShark821", "MountainBlueFalcon157"}


with open(gang_file_path, "r") as file:
    users = {line.strip() for line in file if line.strip() not in exposed_users}

print(f"Loaded {len(users)} gang members.")


hashed_pw_dict = {}
with open(hashed_pw_file_path, "r") as file:
    for line in file:
        parts = line.strip().split(",")
        if len(parts) == 2:
            hashed_pw_dict[parts[0]] = parts[1]  

print(f"Loaded {len(hashed_pw_dict)} hashed credentials.")


with open(pwned_pw_file_path, "r") as file:
    base_passwords = [line.strip() for line in file]

print(f"Loaded {len(base_passwords)} leaked passwords.")


password_variations = [f"{base}{num:02d}" for base in base_passwords for num in range(100)]
print(f"Generated {len(password_variations)} password variations.")


hashed_passwords = {hashlib.sha256(bytes(pw, 'utf-8')).hexdigest(): pw for pw in password_variations}
print(f"Hashed {len(hashed_passwords)} password variations.")


for username, hashed_pw in hashed_pw_dict.items():
    if hashed_pw in hashed_passwords:  
        cracked_password = hashed_passwords[hashed_pw]

        print(f"Trying login for {username}...")  

        
        result = subprocess.run(
            ["python3", login_script_path, username, cracked_password],
            capture_output=True, text=True
        )

        
        if "successful" in result.stdout:
            print(f"Username: {username}, Password: {cracked_password}")
            sys.exit()  


print("No valid username-password combination found.")
sys.exit()
