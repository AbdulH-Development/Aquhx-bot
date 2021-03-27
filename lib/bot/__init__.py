"""
Copyright (c) 2021 DevCairo

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
"""

from discord.ext.commands import Bot as BotBase
from discord.ext.commands import when_mentioned_or
from discord.ext.commands import command
from dotenv import load_dotenv
from discord import Intents
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Cog
from discord import Embed
import platform
import psycopg2
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


PREFIX = when_mentioned_or("$")
OWNER_IDS = [541722893747224589]
color = 0xfffafa


def get_prefix(client, message):
    conn = psycopg2.connect(**dbinfo2)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT prefix FROM db.prefixes WHERE guild_id = %s', (message.guild.id, ))
    prefix = cursor.fetchone()[0]
    return when_mentioned_or(prefix)(client, message)


class Client(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.OWNER = OWNER_IDS
        super().__init__(command_prefix=get_prefix, help_command=None,
                         owners=OWNER_IDS, case_insensitive=True, perms=Intents.all())

    def run(self, version):
        load_dotenv()
        self.TOKEN = os.getenv("AQUHX")
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
client = Client()
VERSION = data['Version']


async def create_db_pool():
    pool = await asyncpg.create_pool(**dbinfo)
    client.db = await pool.acquire()
    
    
class Developer(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.check = "<a:greentick:825189056295862292>"
        self.fail = "<a:redX:825192396655427595>"

    @command(aliases=['reload'])
    async def _reload(self, ctx):
        if ctx.author.id in OWNER_IDS:
            try:
                for cog in os.listdir('./lib/extensions'):
                    if cog.endswith('.py'):
                        self.client.reload_extension(
                            f'lib.extensions.{cog[:-3]}')
                em = Embed(color=color)
                em.description = f"{self.check} Reloaded extensions"
                await ctx.send(embed=em)
            except Exception as e:
                em = Embed(color=color)
                em.description = f"{self.fail} {e}".format(e)
                await ctx.send(embed=em)
        elif ctx.author.id not in OWNER_IDS:
            em = Embed(color=color)
            em.description = f"{self.fail} You don't have permission to run this."
            await ctx.send(embed=em)

    @command(aliases=['restart'])
    async def _restart(self, ctx):
        em = Embed(color=color)
        em.description = f"{self.check} Restarted bot"
        await ctx.send(embed=em)
        if ctx.author.id in OWNER_IDS:
            await self.client.logout()
            await self.client.close()
            if platform.system() == "Windows":
                os.system('python.exe lib/Scripts/non-dev-restart.py')
                os.system('cls')
            elif platform.system() == "Linux":
                os.system('python3 lib/Scripts/non-dev-restart.py')
                os.system('clear')
            elif platform.system() == "Darwin":
                os.system('python3 lib/Scripts/non-dev-restart.py')
                os.system('clear')
        elif ctx.author.id not in OWNER_IDS:
            em = Embed(color=color)
            em.description = f"{self.fail} You don't have permission to run this."
            await ctx.send(embed=em)

    @Cog.listener()
    async def on_member_join(self, member):
        fetch = await self.client.db.fetchrow("SELECT channel_id FROM db.messages WHERE guild_id = $1", member.guild.id)
        if fetch == None:
            return
        elif fetch != None:
            try:
                mention = member.mention
                members = len(list(member.guild.members))
                user = member.name
                welcome = await self.client.db.fetchrow("SELECT welcome FROM db.welcome WHERE guild_id = $1", member.guild.id)
                if welcome == None:
                    return
                channel = self.client.get_channel(int(fetch[0]))
                await channel.send(str(welcome[0]).format(mention=mention, user=user, members=members))
            except Exception as e:
                pass

    @Cog.listener()
    async def on_member_remove(self, member):
        fetch = await self.client.db.fetchrow("SELECT channel_id FROM db.messages WHERE guild_id = $1", member.guild.id)
        if fetch == None:
            return
        elif fetch != None:
            try:
                mention = member.mention
                members = len(list(member.guild.members))
                user = member.name
                welcome = await self.client.db.fetchrow("SELECT goodbye FROM db.goodbye WHERE guild_id = $1", member.guild.id)
                if welcome == None:
                    return
                channel = self.client.get_channel(int(fetch[0]))
                await channel.send(str(welcome[0]).format(mention=mention, user=user, members=members))
            except Exception as e:
                pass

    @Cog.listener()
    async def on_guild_join(self, guild):
        await guild.create_role(name="Muted")
        await self.client.db.execute("INSERT INTO db.prefixes(guild_id, prefix) VALUES($1, $2)", guild.id, "$")

    @Cog.listener()
    async def on_guild_remove(self, guild):
        await self.client.db.execute("DELETE FROM db.prefixes WHERE guild_id = $1", guild.id)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author == self.client.user:
            return
        if after.author.bot:
            return

        result = await self.client.db.fetchrow("SELECT channel_id FROM db.modlog WHERE guild_id = $1", after.guild.id)
        if result == None:
            return
        msg = str(before.content)
        new = msg.replace("https://", "")
        if "https://" + new in before.content:
            return
        elif result != None:
            try:
                channel = self.client.get_channel(int(result[0]))
                em = Embed(color=color)
                em.set_author(
                    name=f"{after.author.name} triggered an event", icon_url=self.client.user.avatar_url)
                em.description = f"""
                {before.author.mention} edited their message\nin {before.channel.mention}.\n\nOld\n```{before.content}```\n\nNew\n```{after.content}```"""
                em.set_thumbnail(url=self.client.user.avatar_url)
                await channel.send(embed=em)
            except Exception as e:
                pass

    @Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.client.user:
            return
        if message.author.bot:
            return
        elif message.author != self.client.user:
            result = await self.client.db.fetchrow('SELECT channel_id FROM db.modlog WHERE guild_id = $1', message.guild.id)
            if result == None:
                return
            elif result != None:
                channel = self.client.get_channel(int(result[0]))
                em = Embed(color=color)
                em.description = f"""
                message by {message.author.mention} deleted\nin {message.channel.mention}\n\nContent\n```{message.content}```
                """
                em.set_thumbnail(url=self.client.user.avatar_url)
                await channel.send(embed=em)


client.add_cog(Developer(client))
asyncio.get_event_loop().run_until_complete(create_db_pool())
