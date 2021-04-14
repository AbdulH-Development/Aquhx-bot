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
from discord.ext.commands import *
from discord.ext import *
from dotenv import load_dotenv
from discord import Intents, Embed
from lib.bot.info import *
import platform
import psycopg2
import mariadb
import asyncio
import math
import json
import os


class Client(BotBase):
    def __init__(self):
        super().__init__(command_prefix=get_prefix, help_command=None,
                         owners=OWNER_IDS, case_insensitive=True, intents=Intents.all())

    def run(self, version):
        try:
            load_dotenv()
            self.TOKEN = os.getenv("AQUHX")
            self.VERSION = version
            super().run(self.TOKEN, reconnect=True)
        except KeyboardInterrupt:
            print("Shutting down")
        except RuntimeError:
            print("Interrupted")

    async def on_ready(self):
        print(f"""
[INFO] Logged in as {self.user}
[INFO] Bot version: 2.0.6
[INFO] Created by: DevCairo
[INFO] Collaboraters Mossyegghead01, AFK_Pilot""")
        for cog in os.listdir("./lib/ext"):
            if cog.endswith('.py'):
                client.load_extension(f"lib.ext.{cog[:-3]}")
                print(f"[INFO] Loaded lib/ext/{cog[:-3]}.py")

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        if hasattr(ctx.command, 'setup'):
            return

        error = getattr(error, 'original', error)

        if isinstance(error, ChannelNotFound):
            em = Embed(color=0xff0000)
            em.description = 'Could not find that channel'
            await ctx.send(embed=em)
            return
        if isinstance(error, CommandOnCooldown):
            em = Embed(color=0xff0000)
            em.description = 'The command you have attempted to execute is on cooldown.\nPlease try again in {}s.'.format(
                math.ceil(error.retry_after))
            await ctx.send(embed=em)
            return
        if isinstance(error, MissingPermissions):
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
        if isinstance(error, BotMissingPermissions):
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
        if isinstance(error, CommandNotFound):
            em = Embed(color=0xff0000)
            em.description = "[ERROR] Unknown command"
            await ctx.send(embed=em)
            return


client = Client()
VERSION = "2.0.6"


async def create_db_pool():
    try:
        client.db = mariadb.connect(**dbinfo)
        client.db.auto_reconnect = True
        client.cursor = client.db.cursor()
        client.cursor.execute("SET SESSION wait_timeout=12000")
    except mariadb.InterfaceError:
        client.db = mariadb.reconnect(**dbinfo)
        client.db.auto_reconnect = True
        client.cursor = client.db.cursor()
    client.color = 0xfffafa
    client.complete = "<a:greentick:825189056295862292>"
    client.fail = "<a:redX:825192396655427595>"


@tasks.loop(seconds=12000)
async def dbstuff():
    client.db = mariadb.connect(**dbinfo)
    client.cursor = client.db.cursor()
    client.cursor.execute("SET SESSION wait_timeout=12000")


dbstuff.start()


class Developer(Cog):
    def __init__(self, client):
        self.client = client
        self.check = "<a:greentick:825189056295862292>"
        self.fail = "<a:redX:825192396655427595>"

    @command(aliases=['reload'])
    async def _reload(self, ctx):
        if ctx.author.id in OWNER_IDS:
            try:
                for cog in os.listdir('./lib/ext'):
                    if cog.endswith('.py'):
                        self.client.reload_extension(
                            f'lib.ext.{cog[:-3]}')
                em = Embed(color=self.client.color)
                em.description = f"{self.check} Reloaded extensions"
                await ctx.send(embed=em)
            except Exception as e:
                em = Embed(color=self.client.color)
                em.description = f"{self.fail} {e}".format(e)
                await ctx.send(embed=em)
        elif ctx.author.id not in OWNER_IDS:
            em = Embed(color=self.client.color)
            em.description = f"{self.fail} You don't have permission to run this."
            await ctx.send(embed=em)

    @command(aliases=['restart'])
    async def _restart(self, ctx):
        if ctx.author.id in OWNER_IDS:
            em = Embed(color=self.client.color)
            em.description = f"{self.check} Restarted bot"
            await ctx.send(embed=em)
            await self.client.logout()
            await self.client.close()
            if platform.system() == "Windows":
                os.system('cls')
                os.system('python.exe main.py')
            elif platform.system() == "Linux":
                os.system('clear')
                os.system('python3 main.py')
            elif platform.system() == "Darwin":
                os.system("clear")
                os.system('python3 main.py')
        elif ctx.author.id not in OWNER_IDS:
            em = Embed(color=self.client.color)
            em.description = f"{self.fail} You don't have permission to run this."
            await ctx.send(embed=em)

    @Cog.listener()
    async def on_member_join(self, member):
        try:
            self.client.cursor.execute(
                "SELECT welchan FROM welcome WHERE guild_id = ?", (member.guild.id, ))
        except mariadb.InterfaceError:
            self.client.db = mariadb.connect(**dbinfo)
            self.client.db.auto_reconnect = True
            self.client.cursor = client.db.cursor()
            self.client.cursor.execute(
                "SELECT welchan FROM welcome WHERE guild_id = ?", (member.guild.id, ))
        fetch = self.client.cursor.fetchone()
        if fetch == None:
            return
        elif fetch != None:
            mention = member.mention
            members = len(list(member.guild.members))
            user = member.name
            guild = member.guild.name
            try:
                self.client.cursor.execute(
                    "SELECT welcome FROM welcome WHERE guild_id = ?", (member.guild.id, ))
            except mariadb.InterfaceError:
                self.client.db = mariadb.connect(**dbinfo)
                self.client.db.auto_reconnect = True
                self.client.cursor = client.db.cursor()
                self.client.cursor.execute(
                    "SELECT welcome FROM welcome WHERE guild_id = ?", (member.guild.id, ))
            welcome = self.client.cursor.fetchone()
            if welcome == None:
                return
            elif welcome != None:
                channel = self.client.get_channel(int(fetch[0]))
                await channel.send(str(welcome[0]) .format(mention=mention, user=user, members=members, guild=guild))

    @Cog.listener()
    async def on_member_remove(self, member):
        try:
            self.client.cursor.execute(
                "SELECT goodchan FROM goodbye WHERE guild_id = ?", (member.guild.id, ))
        except mariadb.InterfaceError:
            self.client.db = mariadb.connect(**dbinfo)
            self.client.db.auto_reconnect = True
            self.client.cursor = client.db.cursor()
            self.client.cursor.execute(
                "SELECT goodchan FROM goodbye WHERE guild_id = ?", (member.guild.id, ))
        fetch = self.client.cursor.fetchone()
        if fetch == None:
            return
        elif fetch != None:
            mention = member.mention
            members = len(list(member.guild.members))
            user = member.name

            try:
                self.client.cursor.execute(
                    "SELECT goodbye FROM goodbye WHERE guild_id = ?", (member.guild.id, ))
            except mariadb.InterfaceError:
                self.client.db = mariadb.connect(**dbinfo)
                self.client.db.auto_reconnect = True
                self.client.cursor = client.db.cursor()
                self.client.cursor.execute(
                    "SELECT goodbye FROM goodbye WHERE guild_id = ?", (member.guild.id, ))
            welcome = self.client.cursor.fetchone()
            if welcome == None:
                return
            elif welcome != None:
                channel = self.client.get_channel(int(fetch[0]))
                await channel.send(str(welcome[0]) .format(mention=mention, user=user, members=members))

    @Cog.listener()
    async def on_member_ban(self, guild, member):
        try:
            self.client.cursor.execute(
                "SELECT channel_id FROM modlog WHERE guild_id = ?", (guild.id,))
        except mariadb.InterfaceError:
            self.client.db = mariadb.connect(**dbinfo)
            self.client.db.auto_reconnect = True
            self.client.cursor = client.db.cursor()
            self.client.cursor.execute(
                "SELECT channel_id FROM modlog WHERE guild_id = ?", (guild.id,))
        fetch = self.client.cursor.fetchone()
        if fetch == None:
            return
        elif fetch != None:
            channel = self.client.get_channel(int(fetch[0]))
            em = Embed(color=self.client.color)
            em.set_author(
                name=f"Member banned", icon_url=member.avatar_url)
            em.description = f"**{member.name}{member.discriminator}** was banned\n from **{guild.name}**"
            em.set_thumbnail(url=member.avatar_url)
            await channel.send(embed=em)

    @Cog.listener()
    async def on_guild_join(self, guild):
        await guild.create_role(name="Muted")
        try:
            self.client.cursor.execute(
                "INSERT INTO prefixes (guild_id, prefix) VALUES (?, ?)", (guild.id, "$",))
        except mariadb.InterfaceError:
            self.client.db = mariadb.connect(**dbinfo)
            self.client.db.auto_reconnect = True
            self.client.cursor = client.db.cursor()
            self.client.cursor.execute(
                "INSERT INTO prefixes (guild_id, prefix) VALUES (?, ?)", (guild.id, "$",))
        self.client.db.commit()

    @Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            self.client.cursor.execute(
                "DELETE FROM prefixes WHERE guild_id = ?", (guild.id, ))
            self.client.cursor.execute(
                "DELETE FROM welcome WHERE guild_id = ?", (guild.id, ))
            self.client.cursor.execute(
                "DELETE FROM goodbye WHERE guild_id = ?", (guild.id, ))
            self.client.cursor.execute(
                "DELETE FROM modlog WHERE guild_id = ?", (guild.id,))
        except mariadb.InterfaceError:
            self.client.db = mariadb.connect(**dbinfo)
            self.client.db.auto_reconnect = True
            self.client.cursor = client.db.cursor()
            self.client.cursor.execute(
                "DELETE FROM prefixes WHERE guild_id = ?", (guild.id, ))
            self.client.cursor.execute(
                "DELETE FROM welcome WHERE guild_id = ?", (guild.id, ))
            self.client.cursor.execute(
                "DELETE FROM goodbye WHERE guild_id = ?", (guild.id, ))
            self.client.cursor.execute(
                "DELETE FROM modlog WHERE guild_id = ?", (guild.id,))
        self.client.db.commit()

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author == self.client.user:
            return
        if before.author.bot:
            return
        try:
            self.client.cursor.execute(
                'SELECT channel_id FROM modlog WHERE guild_id = ?', (before.guild.id,))
        except mariadb.InterfaceError:
            self.client.db = mariadb.connect(**dbinfo)
            self.client.db.auto_reconnect = True
            self.client.cursor = client.db.cursor()
            self.client.cursor.execute(
                'SELECT channel_id FROM modlog WHERE guild_id = ?', (before.guild.id,))
        result = self.client.cursor.fetchone()
        if result == None:
            return
        msg = str(before.content)
        new = msg.replace("https://", "")
        if "https://" + new in before.content:
            return
        elif result != None:
            try:
                channel = self.client.get_channel(int(result[0]))
                em = Embed(color=self.client.color)
                em.set_author(
                    name=f"{after.author.name} triggered an event", icon_url=after.author.avatar_url)
                em.description = f"""
                {before.author.mention} edited their message\nin {before.channel.mention}.\n\nOld\n```{before.content}```\n\nNew\n```{after.content}```"""
                em.set_thumbnail(url=after.author.avatar_url)
                await channel.send(embed=em)
            except Exception as e:
                print(e)

    @Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.client.user:
            return
        if message.author.bot:
            return
        elif message.author != self.client.user:
            try:
                self.client.cursor.execute(
                    'SELECT channel_id FROM modlog WHERE guild_id = ?', (message.guild.id,))
            except mariadb.InterfaceError:
                self.client.db = mariadb.connect(**dbinfo)
                self.client.db.auto_reconnect = True
                self.client.cursor = client.db.cursor()
                self.client.cursor.execute(
                    'SELECT channel_id FROM modlog WHERE guild_id = ?', (message.guild.id,))
            result = self.client.cursor.fetchone()
            if result == None:
                return
            elif result != None:
                channel = self.client.get_channel(int(result[0]))
                em = Embed(color=self.client.color)
                em.set_author(
                    name=f"{message.author.name} triggered an event", icon_url=message.author.avatar_url)
                em.description = f"""
                message by {message.author.mention} deleted\nin {message.channel.mention}\n\nContent\n```{message.content}```
                """
                em.set_thumbnail(url=message.author.avatar_url)
                await channel.send(embed=em)


client.add_cog(Developer(client))
asyncio.get_event_loop().run_until_complete(create_db_pool())
