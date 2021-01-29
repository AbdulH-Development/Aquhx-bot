# First imports

import discord
import time
import os
import aiosqlite
import sqlite3
import sys
from Modules.__loader__ import __load__

# Secondary imports
#colorama is optional, if you dont have colorama the bot will disable it
iscolorama = True
try:
    from colorama import Fore
except ImportError:
    iscolorama = False
    print("Colorama not installed, or something went wrong when importing, turning all colorama feature off.")
from dotenv import load_dotenv
from discord.ext import commands

# Third imports

from discord.ext.commands import Bot
from discord.ext.commands import when_mentioned_or

# Bot constructor

client = Bot(
    command_prefix=when_mentioned_or(';'),
    case_insensitive=True,
    perms=discord.Intents.all())
sys.dont_write_bytecode = True
__load__(client)

# Loads a .env file and runs the bot.

load_dotenv()
client.run(os.getenv("TOKEN"))
