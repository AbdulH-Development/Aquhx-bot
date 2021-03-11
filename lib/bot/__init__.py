from discord.ext.commands import Bot as BotBase
from discord.ext.commands import when_mentioned_or
from discord.ext import commands
from dotenv import load_dotenv
from discord import Intents
from discord import Embed
import asyncio
import asyncpg
import math
import json
import os


load_dotenv()
IP = os.getenv("IP")
load_dotenv()
PASSWD = os.getenv("PASSWD")
load_dotenv()
DB = os.getenv("DB")

PREFIX = when_mentioned_or("$")
OWNER_IDS = [541722893747224589]
dbinfo = {
    'max_inactive_connection_lifetime': 1,
    'user': 'postgres',
    'password': PASSWD,
    'database': DB,
    'host': IP
}


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.OWNER = OWNER_IDS
        super().__init__(command_prefix=PREFIX, help_command=None,
                         owners=OWNER_IDS, case_insensitive=True, perms=Intents.all())

    def run(self, version):
        load_dotenv()
        self.TOKEN = os.getenv("TOKEN")
        self.VERSION = version
        super().run(self.TOKEN, reconnect=True)

    async def on_ready(self):
        f = open('lib/config/config.json', 'r')
        data = json.load(f)
        print(f"""
[INFO] Logged in as {self.user}
[INFO] Bot version: {data['Version']}
[INFO] Created by: {data['Owner']}
[INFO] Collaboraters {data['Collaboraters']}""")
        for filename in os.listdir('./lib/extensions'):
            if filename.endswith('.py'):
                self.load_extension(f'lib.extensions.{filename[:-3]}')
                print(f'[INFO] Loaded lib/extensions/{filename[:-3]}.py')

        try:
            pool = await asyncpg.create_pool(**dbinfo)
            pg_con = await pool.acquire()
            sql = open('lib/config/db/create.sql', 'r')
            await pg_con.execute(sql.read())
        finally:
            await pool.release(pg_con)

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        if hasattr(ctx.command, 'setup'):
            return

        error = getattr(error, 'original', error)

        if isinstance(error, commands.ChannelNotFound):
            em = Embed(color=0xff0000)
            em.description = 'Could not find that channel'
            await ctx.send(embed=em)
            return
        if isinstance(error, commands.CommandOnCooldown):
            em = Embed(color=0xff0000)
            em.description = 'The command you have attempted to execute is on cooldown.\nPlease try again in {}s.'.format(
                math.ceil(error.retry_after))
            await ctx.send(embed=em)
            return
        if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace(
                'guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                perms = '{}, and {}'.format(
                    "**, **".join(missing[:-1]), missing[-1])
            else:
                perms = ' and '.join(missing)
            em = Embed(color=0xff0000)
            em.description = 'You do not have the the **{}** permission(s) which is needed to execute the command'.format(
                perms)
            await ctx.send(embed=em)
            return
        if isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace(
                'guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                perms = '{}, and {}'.format(
                    "**, **".join(missing[:-1]), missing[-1])
            else:
                perms = ' and '.join(missing)
            em = Embed(color=0xff0000)
            em.description = "[ERROR] I am missing the **{}** permission(s) to execute the command".format(
                perms)
            await ctx.send(embed=em)
            return
        if isinstance(error, commands.CommandNotFound):
            em = Embed(color=0xff0000)
            em.description = "[ERROR] Unknown command"
            await ctx.send(embed=em)
            return


f = open('lib/config/config.json', 'r')
data = json.load(f)

client = Bot()
VERSION = data['Version']


async def create_db_pool():
    pool = await asyncpg.create_pool(**dbinfo)
    client.db = await pool.acquire()


asyncio.get_event_loop().run_until_complete(create_db_pool())

