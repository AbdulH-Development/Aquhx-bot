import os
import time
import sys
import sqlite3
from colorama import Fore

sys.dont_write_bytecode = True
def __load__(client):
    """
    Load your extensions
    """
    db = sqlite3.connect("main.py")
    cursor = db.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS portal(
            guild_id TEXT,
            channel_id TEXT,
            welcome TEXT,
            goodbye TEXT
        )
        """)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS logs(
            guild_id TEXT,
            channel_id TEXT
        )
        """
    )
    for filename in os.listdir('./extensions'):
        if filename.endswith('.py'):
            client.load_extension(f'extensions.config')
            client.load_extension(f'extensions.Administrator')
            client.load_extension(f'extensions.tasks')
            print(Fore.GREEN + "[STATUS] Running..." + Fore.RESET)
            time.sleep(0.7)
            print(Fore.GREEN + "[STATUS] Loading extensions" + Fore.RESET)
            time.sleep(15)
            print(Fore.GREEN + "[STATUS] Bot loaded" + Fore.RESET)
            time.sleep(0.9)
            print(Fore.YELLOW + "[WARNING] If you get an error, please fix it in another bot and copy and paste the code back here." + Fore.RESET)
            time.sleep(0.9)
            print(Fore.RESET + "[DONE] Bot succesfully executed." + Fore.RESET)
            return
        else:
            print(Fore.RED + "[ERROR] Process terminated.")
            return