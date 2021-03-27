from discord.ext.commands import command
from discord.ext.commands import Cog
from discord.ext import commands
from ..bot import OWNER_IDS
from discord import Embed
import platform
import os

color = 0xfffafa


class Developer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @command(aliases=['reload'])
    async def _reload(self, ctx):
        if ctx.author.id in OWNER_IDS:
            try:
                for cog in os.listdir('./lib/extensions'):
                    if cog.endswith('.py'):
                        self.client.reload_extension(
                            f'lib.extensions.{cog[:-3]}')
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
                message by {message.author.mention} deleted\nin {message.channel.mention}\nContent\n```{message.content}```
                """
                em.set_thumbnail(url=self.client.user.avatar_url)
                await channel.send(embed=em)

def setup(client):
    client.add_cog(Developer(client))
