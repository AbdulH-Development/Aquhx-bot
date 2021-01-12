# First imports

import discord
import aiosqlite
import asyncio
import math

# Secondary imports

import discord.ext
from discord.ext import commands


color = 0x2e9bbb
errorc = 0xff0000
donec = 0x00c21d


class tasks(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        db = await aiosqlite.connect("sql/main.sqlite")
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS logs(
                channel_id TEXT,
                guild_id TEXT)
            """)
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS prefixes(
                guild_prefix TEXT,
                guild_id TEXT)
            """)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        elif isinstance(error, discord.ext.commands.CommandNotFound):
            em = discord.Embed(color=errorc)
            em.description = "That command does not exist!"
            em.title = "[ERROR] Command not found!"
            await ctx.send(embed=em)
            return
        elif isinstance(error, discord.ext.commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            em = discord.Embed(color=errorc)
            em.description = "You are missing the **{}** permissions to run this command!" .format(fmt)
            em.title = "[ERROR] Missing permissions!"
            await ctx.send(embed=em)
        elif isinstance(error, discord.ext.commands.TooManyArguments):
            em = discord.Embed(color=errorc)
            em.description = "You have provided too many arguments!"
            em.title = "[ERROR] Too many arguments!"
            await ctx.send(embed=em)
        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            em = discord.Embed(color=errorc)
            em.description = "Your are missing a required argument(s)"
            em.title = "[ERROR] Missing required argument!"
            await ctx.send(embed=em)
        elif isinstance(error, discord.ext.commands.CommandOnCooldown):
            em = discord.Embed(color=errorc)
            em.description = "You are on cooldown, retry after **{}**s" .format(math.ceil(error.retry_after))
            em.title = "[ERROR] Command on cooldown!"
            await ctx.send(embed=em)
        elif isinstance(error, discord.ext.commands.MemberNotFound):
            em = discord.Embed(color=errorc)
            em.description = "That member is not in this guild!"
            em.title = "[ERROR] Member not found!"
            await ctx.send(embed=em)
        elif isinstance(error, discord.ext.commands.UserNotFound):
            em = discord.Embed(color=errorc)
            em.description = "That user is not on discord!"
            em.title = "[ERROR] User not found!"
            await ctx.send(embed=em)
        elif isinstance(error, discord.ext.commands.ChannelNotFound):
            em = discord.Embed(color=errorc)
            em.description = "Channel does not exist!"
            em.title = "[ERROR] Channel not found!"
            await ctx.send(embed=em)
        elif isinstance(error, discord.ext.commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            em = discord.Embed(color=errorc)
            em.description = "I am missing the **{}** permissions!" .format(fmt)
            em.title = "[ERROR] I am missing permissions!"
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(tasks(client))
    return