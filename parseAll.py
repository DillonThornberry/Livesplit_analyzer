import os
import subprocess

lssFolder = "./lss/no-lblj/"

file_names = [f for f in os.listdir(lssFolder) if os.path.isfile(os.path.join(lssFolder, f))]

for file_name in file_names:
    subprocess.run(['python', 'parseLss.py', file_name, 'no-lblj'], check=True)
    print(file_name)