import discord
import aiosqlite
import json
from dotenv import load_dotenv
import asyncpg
import os
from discord.ext import commands
from discord.ext.commands import Cog


color = 0xff4500   # 0xfffafa  # 0x4B0082


load_dotenv()
IP = os.getenv("IP")
load_dotenv()
PASSWD = os.getenv("PASSWD")
load_dotenv()
DB = os.getenv("DB")


class config(Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['logsconfig', 'logconfig'])
    @commands.has_permissions(manage_channels=True)
    async def configlogs(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            em = discord.Embed(color=color)
            em.title = "Configlogs command"
            em.description = """
            Requires = Manage channels
            Arguments = channel
            Description = Configures the log channel
            """
            em.set_footer(icon_url=ctx.author.avatar_url,
                          text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=em)
        elif channel != None:
            try:
                pool = await asyncpg.create_pool(user='postgres', password=PASSWD, database=DB, host=IP, max_inactive_connection_lifetime=1)
                pg_con = await pool.acquire()
                result = await pg_con.fetchrow(f"SELECT * FROM aquhx.modlog WHERE guild_id = $1", ctx.guild.id)
                if result is None:
                    await pg_con.execute("INSERT INTO aquhx.modlog(guild_id, channel_id) VALUES($1, $2)",
                                         ctx.guild.id, channel.id)
                    em = discord.Embed(color=color,
                                       description="✅ Set log channel!")
                    await ctx.send(embed=em)

                elif result is not None:
                    await pg_con.execute("UPDATE aquhx.modlog SET channel_id = $1 WHERE guild_id = $2",
                                         channel.id, ctx.guild.id)
                    em = discord.Embed(color=color,
                                       description="✅ Updated log channel!")
                    await ctx.send(embed=em)
            finally:
                await pool.release(pg_con)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def deletelogs(self, ctx):
        pool = await asyncpg.create_pool(user='postgres', password=PASSWD, database=DB, host=IP, max_inactive_connection_lifetime=1)
        pg_con = await pool.acquire()
        result = await pg_con.fetchrow(f"SELECT * FROM aquhx.modlog WHERE guild_id = $1", ctx.guild.id)
        if result is None:

            em = discord.Embed(color=color,
                               description="❌ You haven't configured a log channel!")
            await ctx.send(embed=em)

        elif result is not None:

            await pg_con.execute("DELETE FROM aquhx.modlog WHERE guild_id = $1", ctx.guild.id)
            em = discord.Embed(color=color,
                               description="✅ Removed the log channel!")
            await ctx.send(embed=em)
        await pool.release(pg_con)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def channelconfig(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            em = discord.Embed(color=color)
            em.title = "Channelconfig command"
            em.description = """
            Requires = Manage channels
            Arguments = channel
            Description = Configures the messages channel
            """
            em.set_footer(icon_url=ctx.author.avatar_url,
                          text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=em)
        elif channel != None:
            try:
                pool = await asyncpg.create_pool(user='postgres', password=PASSWD, database=DB, host=IP, max_inactive_connection_lifetime=1)
                pg_con = await pool.acquire()
                result = await pg_con.fetchrow(f"SELECT * FROM aquhx.messages WHERE guild_id = $1", ctx.guild.id)
                if result == None:
                    await pg_con.execute("INSERT INTO aquhx.messages(guild_id, channel_id) VALUES($1, $2)", ctx.guild.id, channel.id)
                    em = discord.Embed(color=color,
                                       description="✅ Set messages channel!")
                    await ctx.send(embed=em)
                elif result != None:
                    await pg_con.execute("UPDATE aquhx.messages SET channel_id = $1 WHERE guild_id = $2", channel.id, ctx.guild.id)
                    em = discord.Embed(color=color,
                                       description="✅ Updated messages channel!")
                    await ctx.send(embed=em)
            finally:
                await pool.release(pg_con)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def deletechannel(self, ctx):
        pool = await asyncpg.create_pool(user='postgres', password=PASSWD, database=DB, host=IP, max_inactive_connection_lifetime=1)
        pg_con = await pool.acquire()
        result = await pg_con.fetchrow(f"SELECT * FROM aquhx.messages WHERE guild_id = $1", ctx.guild.id)
        if result is None:

            em = discord.Embed(color=color,
                               description="❌ You haven't configured a messages channel!")
            await ctx.send(embed=em)

        elif result is not None:

            await pg_con.execute("DELETE FROM aquhx.messages WHERE guild_id = $1", ctx.guild.id)
            em = discord.Embed(color=color,
                               description="✅ Removed the messages channel!")
            await ctx.send(embed=em)
        await pool.release(pg_con)


def setup(client):
    client.add_cog(config(client))
