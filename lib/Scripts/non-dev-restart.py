import os
import platform


if platform.system() == "Linux":
    os.system('python3 main.py')
elif platform.system() == "Windows":
    os.system('python.exe main.py')
elif platform.system() == "Darwin":
    os.system('python3 main.py')
