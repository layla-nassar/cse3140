import time
import subprocess
import hashlib

start = time.time()
print("Start time: 0 seconds")

PwnedPWs100k = open('PwnedPWs100k', 'r')
passwords=[]
for password in PwnedPWs100k:
   passwords.append(password.strip()) 

gang_file = open('gang', 'r')
gang=[]
for users in gang_file:
   gang.append(users.strip())

salted_gang = {}
with open('SaltedPWs', 'r') as saltedpws:
    for line in saltedpws:
        user, salt, hashed_pw = line.strip().split(',')
        if user in gang:  
            salted_gang[user] = (salt, hashed_pw)

matches = []
for password in passwords:
    for j in range(0,9):  
        test_pw = password + str(j)
        for user, (salt, stored_hash) in salted_gang.items():
            hashed_test_pw = hashlib.sha256(bytes(salt + test_pw, 'utf-8')).hexdigest()
            
            if hashed_test_pw == stored_hash:
                matches.append((user, test_pw))

for user, password in matches:
    result = subprocess.run(["python3", "Login.pyc", user, password], capture_output=True, text=True)
    if "successful" in result.stdout:
        print(f"Username {user} Password {password}")

end = time.time() - start
print(f"{end:.2f} seconds")
