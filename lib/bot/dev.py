from discord.ext.commands import Bot as BotBase
from discord.ext.commands import when_mentioned_or
from discord.ext.commands import command
from dotenv import load_dotenv
from discord import Intents
from discord import Embed
from discord.ext import commands
from discord import Embed
import platform
import psycopg2
import asyncio
import asyncpg
import math
import time
import json
import os


load_dotenv()
IP = os.getenv("IP")
load_dotenv()
PASSWD = os.getenv("PASSWD")
load_dotenv()
DB = os.getenv("DB")


dbinfo = {
    'user': 'postgres',
    'host': IP,
    'password': PASSWD,
    'database': DB,
    'max_inactive_connection_lifetime': 5
}

dbinfo2 = {
    'user': 'postgres',
    'host': IP,
    'password': PASSWD,
    'database': DB,
    'port': 5432
}


PREFIX = when_mentioned_or(".")
OWNER_IDS = [541722893747224589]
color = 0xfffafa



class Client(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.OWNER = OWNER_IDS
        super().__init__(command_prefix=PREFIX, help_command=None,
                         owners=OWNER_IDS, case_insensitive=True, perms=Intents.all())

    def run(self, version):
        load_dotenv()
        self.TOKEN = os.getenv("BETA")
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

    async def on_guild_join(self, guild):
        await guild.create_role(name="Muted")
        try:
            pool = await asyncpg.create_pool(**dbinfo)
            pg_con = await pool.acquire()
            await pg_con.execute("INSERT INTO aquhx.prefixes(guild_id, prefix) VALUES($1, $2)", guild.id, "$")
        finally:
            await pool.release(pg_con)

    async def on_guild_remove(self, guild):
        try:
            pool = await asyncpg.create_pool(**dbinfo)
            pg_con = await pool.acquire()
            await pg_con.execute("DELETE FROM aquhx.prefixes WHERE guild_id = $1", guild.id)
        finally:
            await pool.release(pg_con)


    async def on_message_edit(self, before, after):
        if before.author == self.user:
            return
        for guild in self.guilds:
            pool = await asyncpg.create_pool(**dbinfo)
            pg_con = await pool.acquire()
            result = await pg_con.fetchrow("SELECT channel_id FROM aquhx.modlog WHERE guild_id = $1", guild.id)
            if result == None:
                break
            elif result != None:
                try:
                    channel = self.get_channel(int(result[0]))
                    em = Embed(color=color)
                    em.set_author(name=f"{after.author.name} triggered an event", icon_url=self.user.avatar_url)
                    em.description = f"""
                    {before.author.mention} edited their message
                    in {before.channel.mention}.

                    Old
                    ```{before.content}```

                    New 
                    ```{after.content}```
                    """
                    em.set_thumbnail(url=self.user.avatar_url)
                    await channel.send(embed=em)
                except Exception as e:
                    print(e)



    async def on_message_delete(self, message):
        pool = await asyncpg.create_pool(**dbinfo)
        pg_con = await pool.acquire()
        if message.author == self.user:
            return
        result = await pg_con.fetchrow('SELECT channel_id FROM aquhx.modlog WHERE guild_id = $1', message.guild.id)
        if result == None:
            return
        elif result != None:
            try:
                channel = self.get_channel(int(result[0]))
                em = Embed(color=color)
                em.description = f"""
                {message.author.mention} deleted a message
                in {message.channel.mention}

                Content
                ```{message.content}```
                """
                em.set_thumbnail(url=self.user.avatar_url)
                em.set_footer(text=f"")
                await channel.send(embed=em)
            except Exception as e:
                print(e)
        

    async def on_member_join(self, member):
        result = await self.client.db.fetchrow("SELECT channel_id FROM aquhx.messages WHERE guild_id = $1", member.guild.id)
        if result == None:
            return
        elif result != None:
            try:
                mention = member.mention
                members = len(list(member.guild.members))
                user = member.name
                channel = self.get_channel(int(result[0]))
                welcome = self.client.db.fetchrow("SELECT welcome FROM aquhx.welcome WHERE guild_id = $1", member.guild.id)
                await channel.send(str(welcome[0]) .format(members=members, mention=mention, user=user))
            except Exception as e:
                print(e)
            

f = open('lib/config/config.json', 'r')
data = json.load(f)
client = Client()
VERSION = data['Version']


class Developer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @command(aliases=['reload'])
    async def _reload(self, ctx):
        if ctx.author.id in OWNER_IDS:
            try:
                for cog in os.listdir('./lib/extensions'):
                    if cog.endswith('.py'):
                        client.reload_extension(f'lib.extensions.{cog[:-3]}')
                em = Embed(color=color)
                em.description = "✅ Reloaded extensions"
                await ctx.send(embed=em)
            except Exception as e:
                em = Embed(color=color)
                em.description = "❌ {}".format(e)
                await ctx.send(embed=em)
        elif ctx.author.id not in OWNER_IDS:
            em = Embed(color=color)
            em.description = "❌ You don't have permission to run this."
            await ctx.send(embed=em)

    @command(aliases=['restart'])
    async def _restart(self, ctx):
        em = Embed(color=color)
        em.description = "✅ Restarted bot"
        await ctx.send(embed=em)
        if ctx.author.id in OWNER_IDS:
            await self.client.logout()
            await self.client.close()
            if platform.system() == "Windows":
                os.system('python.exe lib/Scripts/dev-restart.py')
                os.system('cls')
            elif platform.system() == "Linux":
                os.system('python3 lib/Scripts/dev-restart.py')
                os.system('clear')
            elif platform.system() == "Darwin":
                os.system('python3 lib/Scripts/dev-restart.py')
                os.system('clear')
        elif ctx.author.id not in OWNER_IDS:
            em = Embed(color=color)
            em.description = "❌ You don't have permission to run this."
            await ctx.send(embed=em)

client.add_cog(Developer(client))


async def create_db_pool():
    pool = await asyncpg.create_pool(**dbinfo)
    client.db = await pool.acquire()


asyncio.get_event_loop().run_until_complete(create_db_pool())
