import subprocess
import os

user_input = input('Enter command: ')
subprocess.call(user_input, shell=True)
password = 'SuperSecret123'
eval(user_input)
os.system(f"echo {user_input} > /tmp/file.txt")