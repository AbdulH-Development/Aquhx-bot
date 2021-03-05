"""
Copyright (c) 2021 Abdul H

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

=================================================================================

If you are using the lib/config/config.json 
make sure you have your Inst package (optional)
manager set to .json instead of .inst in the
configuration folder
"""

# DON'T EDIT THIS

import discord
import os
import asyncpg
import aiosqlite
import json
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import when_mentioned_or


# DON'T EDIT THIS
client = commands.Bot(
    command_prefix=when_mentioned_or('$'),
    case_insensitive=True,
    perms=discord.Intents.all(),
    help_command=None)


# Gets the info for the database

load_dotenv()
IP = os.getenv("IP")
load_dotenv()
PASSWD = os.getenv("PASSWD")
load_dotenv()
DB = os.getenv("DB")


# on_ready event with DB creation

@client.event
async def on_ready():
    f = open('lib/config/config.json', 'r')
    data = json.load(f)
    try:
        sql = open('lib/config/db/create.sql', 'r')
        pool = await asyncpg.create_pool(user='postgres', password=PASSWD, database=DB, host=IP, max_inactive_connection_lifetime=1)
        pg_con = await pool.acquire()
        await pg_con.execute(sql.read())
        for filename in os.listdir('./lib/extensions'):
            if filename.endswith('.py'):
                client.load_extension(f'lib.extensions.{filename[:-3]}')
                print(f'[INFO] Loaded lib/extensions/{filename[:-3]}.py')

    finally:
        await pool.release(pg_con)
    print(
        f"""
[INFO] Logged in as: {client.user}
[INFO] Bot version: {data['Version']}
[INFO] Created by: {data['Owner']}
[INFO] Collaboraters {data['Collaboraters']}
""")


# Reads token from the .env file we set up
load_dotenv()
client.run(os.getenv("TOKEN"))
