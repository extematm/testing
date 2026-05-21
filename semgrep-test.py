import subprocess

user_input = input("cmd: ")

subprocess.run(user_input, shell=True)