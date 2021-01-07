import discord
import time
import os
import sys
from dotenv import load_dotenv
from colorama import Fore
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import when_mentioned_or


client = Bot(
    command_prefix=when_mentioned_or(";"),
    case_insensitive=True,
    help_command=None,
    perms=discord.Intents.all())
sys.dont_write_bytecode = True


@client.event
async def on_ready():
    files = next(os.walk("C:\\Repos\\Aquhx-bot\\extensions")) # CHANGE DIRECTORIES
    file_count = len(files)
    for filename in os.listdir('./extensions'):
        if filename.endswith('.py'):
            client.load_extension(f'extensions.{filename[:-3]}')
            print(Fore.GREEN + "[STATUS] Running..." + Fore.RESET)
            time.sleep(0.7)
            print(Fore.GREEN + "[STATUS] Loading files/folders" + Fore.RESET)
            time.sleep(0.7)
            print(Fore.GREEN + f"[STATUS] Loaded {file_count} files." + Fore.RESET)
            time.sleep(15)
            print(Fore.GREEN + "[STATUS] Bot loaded" + Fore.RESET)
            time.sleep(0.9)
            print(Fore.YELLOW + "[WARNING] If you get an error, please fix it in another bot and copy and paste the code back here." + Fore.RESET)
            time.sleep(0.9)
            print(Fore.RESET + "[DONE] Bot succesfully executed." + Fore.RESET)




load_dotenv()
client.run(os.getenv("TOKEN"))