import os

def find_py_files():
    py_files = []
    for file in os.listdir('.'):
        if file.endswith('.py') and os.path.isfile(file):
            py_files.append(file)
    with open('Q1A.out', 'w') as f:
        f.write('\n'.join(py_files))

if __name__ == "__main__":
    find_py_files()
