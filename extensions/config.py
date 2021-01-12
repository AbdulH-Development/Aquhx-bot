# First imports

import discord
import aiosqlite
import asyncio

# Secondary imports

from discord.ext import commands


color = 0x2e9bbb
errorc = 0xff0000
donec = 0x00c21d


class config(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def logconfig(self, ctx, channel : discord.TextChannel=None):
        db = await aiosqlite.connect("sql/main.sqlite")
        cursor = await db.execute(f"SELECT channel_id FROM logs WHERE guild_id = {ctx.guild.id}")
        result = await cursor.fetchone()
        if channel == None:
            em = discord.Embed(color=color)
            em.title = "Logconfig command"
            em.description = ";Logconfig {channel}"
        elif result is None:
            sql = ("INSERT INTO logs(guild_id, channel_id) VALUES(?,?)")
            val = (ctx.guild.id, channel.id)
            em = discord.Embed(color=color)
            em.description = f"✅ Set log channel to {channel.mention}"
        elif result is not None:
            sql = ("UPDATE logs SET channel_id = ? WHERE guild_id = ?")
            val = (channel.id, ctx.guild.id)
            em = discord.Embed(color=color)
            em.description = f"✅ Updated log channel to {channel.mention}"
        else:
            em = discord.Embed(color=errorc)
            em.title = "Uh oh!"
            em.description = "An unknown error occured!"
        await ctx.send(embed=em)
        await cursor.execute(sql, val)
        await db.commit()
        await cursor.close()
        await db.close()



    @commands.command(aliases=["welcome-config", "wc", "welcome-config"])
    @commands.has_permissions(manage_server=True)
    async def welcomeconfig(self, ctx, *, text=None):
        db = await aiosqlite.connect("main.py")
        cursor = await db.execute(f"SELECT welcome FROM portal WHERE guild_id = {ctx.guild.id}")
        result = await cursor.fetchone()
        if text == None:
            em = discord.Embed(color=color)
            em.title = "Welcomeconfig command"
            em.description = ";Welcomeconfig {text}"
        elif result is None:
            sql = ("INSERT INTO portal(guild_id, welcome) VALUES(?,?)")
            val = (ctx.guild.id, text)
            em = discord.Embed(color=donec)
            em.description = f"✅ Set the welcome message."
        elif result is not None:
            sql = ("UPDATE portal SET welcome = ? WHERE guild_id = ?")
            val = (text, ctx.guild.id)
            em = discord.Embed(color=donec)
            em.description = f"✅ Updated the welcome message."
        await ctx.send(embed=em)
        await cursor.execute(sql, val)
        await db.commit()
        await cursor.close()
        await db.close()



    @commands.command(aliases=["goodbye-config", "gc", "goodbye-config"])
    @commands.has_permissions(manage_server=True)
    async def goodbyeconfig(self, ctx, *, text=None):
        db = await aiosqlite.connect("main.py")
        cursor = await db.execute(f"SELECT goodbye FROM portal WHERE guild_id = {ctx.guild.id}")
        result = await cursor.fetchone()
        if text == None:
            em = discord.Embed(color=color)
            em.title = "Goodbye command"
            em.description = ";Goodbye {text}"
        elif result is None:
            sql = ("INSERT INTO portal(guild_id, goodbye) VALUES(?,?)")
            val = (ctx.guild.id, text)
            em = discord.Embed(color=donec)
            em.description = f"✅ Set the goodbye message."
        elif result is not None:
            sql = ("UPDATE portal SET goodbye = ? WHERE guild_id = ?")
            val = (text, ctx.guild.id)
            em = discord.Embed(color=donec)
            em.description = f"✅ Updated the goodbye message."
        await ctx.send(embed=em)
        await cursor.execute(sql, val)
        await db.commit()
        await cursor.close()
        await db.close()


    @commands.command(aliases=["channel-config", "cc", "channel_config"])
    @commands.has_permissions(manage_server=True)
    async def channelconfig(self, ctx, channel : discord.TextChannel=None):
        db = await aiosqlite.connect("main.py")
        cursor = await db.execute(f"SELECT welcome FROM portal WHERE guild_id = {ctx.guild.id}")
        result = await cursor.fetchone()
        if channel == None:
            em = discord.Embed(color=color)
            em.title = "Channelconfig command"
            em.description = ";Channelconfig {channel}"
        elif result is None:
            sql = ("INSERT INTO portal(guild_id, channel_id) VALUES(?,?)")
            val = (ctx.guild.id, channel.id)
            em = discord.Embed(color=donec)
            em.description = f"✅ Set the channel."
        elif result is not None:
            sql = ("UPDATE portal SET welcome = ? WHERE guild_id = ?")
            val = (channel.id, ctx.guild.id)
            em = discord.Embed(color=donec)
            em.description = f"✅ Updated the channel."
        await ctx.send(embed=em)
        await cursor.execute(sql, val)
        await db.commit()
        await cursor.close()
        await db.close()



    


def setup(client):
    client.add_cog(config(client))
    return