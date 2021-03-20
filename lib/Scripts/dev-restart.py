import os
import platform


if platform.system() == "Linux":
    os.system('python3 dev.py')
elif platform.system() == "Windows":
    os.system('python.exe dev.py')
elif platform.system() == "Darwin":
    os.system('python3 dev.py')



