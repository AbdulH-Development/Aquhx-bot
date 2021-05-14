"""
copyright (c) 2021-present DevCairo
license GPL v3, see LICENSE for more details.
"""

from discord.ext.commands import Bot as Base
from discord.ext.commands import *
from discord.ext import tasks
from colorama import Fore
from discord.ext import *
from discord import *
import warnings
import platform
import aiomysql
import asyncio
import mariadb
import toml
import os


def getServerPrefix(client, message):
        f = open("config.toml", 'r')
        data = toml.load(f)
        conn = mariadb.connect(
            host=data["database"]["server"],
            user= data["database"]["user"],
            password= data["database"]["password"],
            db= data["database"]["database"],
            autocommit= True
        )
        cursor = conn.cursor()
        cursor.execute(
            'SELECT prefix FROM prefixes WHERE guild_id = ?', (message.guild.id, ))
        prefix = cursor.fetchone()
        if prefix:
            prefix = prefix[0]
        else:
            cursor.execute("INSERT INTO prefixes(guild_id, prefix) VALUES(?, ?)", (message.guild.id, "$", ))
            cursor.execute(
                'SELECT prefix FROM prefixes WHERE guild_id = ?', (message.guild.id,))
            prefix = cursor.fetchone()
            if prefix:
                prefix = prefix[0]
        return when_mentioned_or(prefix)(client, message)


class Ext(Base):
    def __init__(self, *args, **kwargs):
        super().__init__()
    
    f = open("config.toml", 'r')
    data = toml.load(f)
    logaccess = {
        "host": data["database"]["server"],
        "user": data["database"]["user"],
        "password": data["database"]["password"],
        "db": data["database"]["database"],
        "autocommit": True
    }


class Client(Base):
    def __init__(self):
        config = open("config.toml", 'r')
        data = toml.load(config)
        super().__init__(command_prefix=getServerPrefix, help_command=None,
                         description=data["client"]["description"], intents=Intents.all())

        self.database.start()
        self.loadCogs()
        self.check = "<a:success:836127425511292979>"
        self.fail = "<a:error:836127425662156840>"
        self.color = 0xcc241d


    def loadCogs(self):
        try:
            for cog in os.listdir("lib/ext"):
                if cog.endswith(".py"):
                    self.load_extension(f"lib.ext.{cog[:-3]}")
                    print("[ " + Fore.GREEN + "OK" + Fore.RESET + f" ] Loaded {cog}" + Fore.RESET)
        except Exception as e:
            print("[ " + Fore.RED + "ERR" + Fore.RESET + f"] {e}")

    @tasks.loop(seconds=12000)
    async def database(self):
        try:
            self.db = await aiomysql.connect(**Ext.logaccess)
            self.cursor = await self.db.cursor()
            print("[ " + Fore.GREEN + "OK" + Fore.RESET +
                  f" ] Created database connection" + Fore.RESET)
            await self.cursor.execute("SET SESSION wait_timeout=12000")
        except Exception as e:
            print(f"[ " + Fore.RED + "ERR!" + Fore.RESET + f" ] {e}")

    def start(self):
        try:
            config = open("config.toml", 'r')
            data = toml.load(config)
            token = data["client"]["token"]
            super().run(token, reconnect=True)
        except KeyboardInterrupt:
            return


    async def on_ready(self):
        try:
            print("[ " + Fore.GREEN + "OK" + Fore.RESET + f" ] Loggined as {self.user}")
        except Exception as e:
            print("[ " + Fore.RED + "ERR" + Fore.RESET + f" ] {e}")

    
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        if hasattr(ctx.command, 'reload'):
            return
        


        error = getattr(error, 'original', error)
    

        f = open("config.toml", 'r')
        err = toml.load(f)

        if isinstance(error, CommandNotFound):
            em = Embed(color=self.color)
            em.title = f"{self.fail} Error! Terminated program"
            em.description = f"{err['error']['cmdnf']} Command not found"
            await ctx.send(embed=em)
            


client = Client()
warnings.filterwarnings('ignore', module=r"aiomysql")


class Developer(Cog):
    def __init__(self, client):
        self.client = client

    @command()
    async def reload(self, ctx):
        if ctx.author.id == 541722893747224589:
            try:
                await ctx.message.delete()
                em = Embed(color=self.client.color)
                em.description = f"{self.client.check} Reloaded cogs"
                await ctx.send(embed=em)
                for cog in os.listdir("lib/ext"):
                    if cog.endswith(".py"):
                        self.client.reload_extension(f"lib.ext.{cog[:-3]}")
                        print(f"[ " + Fore.GREEN + "OK" + Fore.RESET + f" ] Reloaded {cog}")
            except (KeyboardInterrupt, RuntimeError):
                pass
    
    @command()
    async def restart(self, ctx):
        if ctx.author.id == 541722893747224589:
            try:
                await ctx.message.delete()
                em = Embed(color=self.client.color)
                em.description = f"{self.client.check} Restarting bot"
                await ctx.send(embed=em)
                await self.client.close()
                if platform.system() == "Windows":
                    os.system("cls")
                    os.system("python.exe main.py")
                elif platform.system() == "Linux":
                    os.system("clear")
                    os.system("python3 main.py")
                elif platform.system() == "Darwin":
                    os.system("clear")
                    os.system("python3 main.py")
            except (KeyboardInterrupt, RuntimeError):
                pass



client.add_cog(Developer(client))
if __name__ == "__main__":
    try:
        client()
    except (KeyboardInterrupt, RuntimeError, TypeError):
        print()

