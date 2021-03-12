import discord
import aiosqlite
import json
from dotenv import load_dotenv
import asyncpg
import os
import asyncio
from discord.ext import commands
from discord.ext.commands import Cog


color = 0xfffafa  # 0xff4500    0xfffafa  # 0x4B0082


load_dotenv()
IP = os.getenv("IP")
load_dotenv()
PASSWD = os.getenv("PASSWD")
load_dotenv()
DB = os.getenv("DB")


class config(Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setup(self, ctx):
        em = discord.Embed(color=color)
        em.set_author(name="Aquhx setup wizard")
        em.description = """
        Welcome to the Aquhx setup wizard,
        please select a channel to setup by using the name.
        **logs** : Configure your log channel.
        **addmsgs** : Configure your welcome/goodbye messages and channel.
        **dellogs** : Remove the log channel from the database.
        **delmsgs** : Remove the welcome/goodbye channel and messages from the database.
        """
        em.set_footer(text="Aquhx setup wizard",
                      icon_url=self.client.user.avatar_url)
        sent = await ctx.send(embed=em)

        try:
            pool = await asyncpg.create_pool(user='postgres', password=PASSWD, database=DB, host=IP, max_inactive_connection_lifetime=5)
            pg_con = await pool.acquire()
            msg = await self.client.wait_for(
                'message',
                timeout=60.0,
                check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
            if msg:
                if msg.content == "logs":
                    logs = discord.Embed(color=color)
                    logs.set_author(name="Aquhx log wizard")
                    logs.description = "Welcome to the log wizard,\nplease provide me with a channel ID\nExample. 818598634823090197 <- if you try to use that it won't work for you."
                    logs.set_footer(text="Aquhx log wizard",
                                    icon_url=self.client.user.avatar_url)
                    await sent.edit(embed=logs)
                    try:
                        await msg.delete()
                        ID = await self.client.wait_for(
                            'message',
                            timeout=60.0,
                            check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                        if ID:
                            try:
                                log = ID.content
                                await ID.delete()
                                res = await pg_con.fetchrow("SELECT channel_id FROM aquhx.modlog WHERE guild_id = $1", ctx.guild.id)
                                if res == None:
                                    await pg_con.execute("INSERT INTO aquhx.modlog(guild_id, channel_id) VALUES($1, $2)", ctx.guild.id, int(log))
                                    em = discord.Embed(color=color,
                                                       description="✅ Set logs channel!")
                                    await sent.edit(embed=em)
                                elif res != None:
                                    await pg_con.execute("UPDATE aquhx.modlog SET channel_id = $1 WHERE guild_id = $2", int(log), ctx.guild.id)
                                    em = discord.Embed(color=color,
                                                       description="✅ Updated logs channel!")
                                    await sent.edit(embed=em)
                            except Exception as e:
                                await ctx.send("{}".format(e))
                    except asyncio.TimeoutError:
                        await ctx.send("Took too long!")

                elif msg.content == "addmsgs":
                    logs = discord.Embed(color=color)
                    logs.set_author(name="Aquhx msgs wizard")
                    logs.description = "Welcome to the msgs wizard,\nplease provide me with a channel ID\nExample. 818598634823090197 <- if you try to use that it won't work for you."
                    logs.set_footer(text="Aquhx msgs wizard",
                                    icon_url=self.client.user.avatar_url)
                    await sent.edit(embed=logs)
                    try:
                        await msg.delete()
                        ID = await self.client.wait_for(
                            'message',
                            timeout=60.0,
                            check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                        if ID:
                            n = ID.content
                            await ID.delete()
                            res = await pg_con.fetchrow("SELECT channel_id FROM aquhx.messages WHERE guild_id = $1", ctx.guild.id)
                            if res == None:
                                await pg_con.execute("INSERT INTO aquhx.messages(guild_id, channel_id) VALUES($1, $2)", ctx.guild.id, int(n))
                                em = discord.Embed(color=color)
                                em.set_author(name="Aquhx msgs wizard")
                                em.description = "✅ Set the message channel"
                                em.set_footer(
                                    text="Aquhx msgs wizard", icon_url=self.client.user.avatar_url)
                            elif res != None:
                                await pg_con.execute("UPDATE aquhx.messages SET channel_id = $1 WHERE guild_id = $2", int(n), ctx.guild.id)
                                em = discord.Embed(color=color)
                                em.set_author(name="Aquhx msgs wizard")
                                em.description = "✅ Set the message channel"
                                em.set_footer(
                                    text="Aquhx msgs wizard", icon_url=self.client.user.avatar_url)
                            await sent.edit(embed=em)
                            await asyncio.sleep(3)
                            logs = discord.Embed(color=color)
                            logs.set_author(name="Aquhx msgs wizard")
                            logs.description = "Next I require a welcome message."
                            logs.set_footer(text="Aquhx msgs wizard",
                                            icon_url=self.client.user.avatar_url)
                            await sent.edit(embed=logs)
                            try:
                                wel = await self.client.wait_for(
                                    'message',
                                    timeout=60.0,
                                    check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                                if wel:
                                    try:
                                        await wel.delete()
                                        msgs = wel.content
                                        res = await pg_con.fetchrow("SELECT msg FROM aquhx.welcome WHERE guild_id = $1", ctx.guild.id)
                                        if res == None:
                                            await pg_con.execute("INSERT INTO aquhx.welcome(guild_id, msg) VALUES($1, $2)", ctx.guild.id, msgs)
                                            logs = discord.Embed(color=color)
                                            logs.set_author(
                                                name="Aquhx msgs wizard")
                                            logs.description = "✅ Set the welcome message!"
                                            logs.set_footer(text="Aquhx msgs wizard",
                                                            icon_url=self.client.user.avatar_url)
                                            await sent.edit(embed=logs)
                                        elif res != None:
                                            await pg_con.execute("UPDATE aquhx.welcome SET msg = $1 WHERE guild_id = $2", msgs, ctx.guild.id)
                                            logs = discord.Embed(color=color)
                                            logs.set_author(
                                                name="Aquhx msgs wizard")
                                            logs.description = "✅ Updated the welcome message!"
                                            logs.set_footer(text="Aquhx msgs wizard",
                                                            icon_url=self.client.user.avatar_url)
                                            await sent.edit(embed=logs)
                                        await asyncio.sleep(3)
                                        logs = discord.Embed(color=color)
                                        logs.set_author(
                                            name="Aquhx msgs wizard")
                                        logs.description = "Next I require a goodbye message."
                                        logs.set_footer(text="Aquhx msgs wizard",
                                                        icon_url=self.client.user.avatar_url)
                                        await sent.edit(embed=logs)
                                        try:
                                            good = await self.client.wait_for(
                                                'message',
                                                timeout=60.0,
                                                check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                                            if good:
                                                try:
                                                    msgs = good.content
                                                    await good.delete()
                                                    res = await pg_con.fetchrow("SELECT msg FROM aquhx.goodbye WHERE guild_id = $1", ctx.guild.id)
                                                    if res == None:
                                                        await pg_con.execute("INSERT INTO aquhx.goodbye(guild_id, msg) VALUES($1, $2)", ctx.guild.id, msgs)
                                                        logs = discord.Embed(
                                                            color=color)
                                                        logs.set_author(
                                                            name="Aquhx msgs wizard")
                                                        logs.description = "✅ Set goodbye message."
                                                        logs.set_footer(text="Aquhx msgs wizard",
                                                                        icon_url=self.client.user.avatar_url)
                                                        await sent.edit(embed=logs)
                                                    elif res != None:
                                                        await pg_con.execute("UPDATE aquhx.goodbye SET msg = $1 WHERE guild_id = $2", msgs, ctx.guild.id)
                                                        logs = discord.Embed(
                                                            color=color)
                                                        logs.set_author(
                                                            name="Aquhx msgs wizard")
                                                        logs.description = "✅ Updated goodbye message."
                                                        logs.set_footer(text="Aquhx msgs wizard",
                                                                        icon_url=self.client.user.avatar_url)
                                                        await sent.edit(embed=logs)
                                                    await asyncio.sleep(3)
                                                    em = discord.Embed(
                                                        color=color)
                                                    em.set_author(
                                                        name="Aquhx msgs wizard")
                                                    em.description = "✅ Completed all tasks, thank you for using Aquhx"
                                                    em.set_footer(
                                                        text="Aquhx msgs wizard", icon_url=self.client.user.avatar_url)
                                                    await sent.edit(embed=em)
                                                except Exception as e:
                                                    await ctx.send("{}" .format(e))
                                        except asyncio.TimeoutError:
                                            logs = discord.Embed(color=color)
                                            logs.set_author(
                                                name="Aquhx msgs wizard")
                                            logs.description = "Do you want to continue without a goodbye message? Y, N"
                                            logs.set_footer(text="Aquhx msgs wizard",
                                                            icon_url=self.client.user.avatar_url)
                                            await sent.edit(embed=logs)
                                            try:
                                                answer = await self.client.wait_for(
                                                    'message',
                                                    timeout=60.0,
                                                    check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                                                if answer:
                                                    await answer.delete()
                                                    try:
                                                        if answer == "Y" or 'y':
                                                            em = discord.Embed(
                                                                color=color)
                                                            em.set_author(
                                                                name="Aquhx msgs wizard")
                                                            em.description = "✅ Completed all tasks, thank you for using Aquhx"
                                                            em.set_footer(
                                                                text="Aquhx msgs wizard", icon_url=self.client.user.avatar_url)
                                                            await sent.edit(embed=em)
                                                        elif answer == "N" or 'n':
                                                            try:
                                                                good = await self.client.wait_for(
                                                                    'message',
                                                                    timeout=60.0,
                                                                    check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                                                                if good:
                                                                    try:
                                                                        await good.delete()
                                                                        res = await pg_con.fetchrow("SELECT msg FROM aquhx.goodbye WHERE guild_id = $1", ctx.guild.id)
                                                                        if res == None:
                                                                            await pg_con.execute("INSERT INTO aquhx.goodbye(guild_id, msg) VALUES($1, $2)", ctx.guild.id, msgs)
                                                                            logs = discord.Embed(
                                                                                color=color)
                                                                            logs.set_author(
                                                                                name="Aquhx msgs wizard")
                                                                            logs.description = "✅ Set goodbye message."
                                                                            logs.set_footer(text="Aquhx msgs wizard",
                                                                                            icon_url=self.client.user.avatar_url)
                                                                            await sent.edit(embed=logs)
                                                                        elif res != None:
                                                                            await pg_con.execute("UPDATE aquhx.goodbye SET msg = $1 WHERE guild_id = $2", msgs, ctx.guild.id)
                                                                            logs = discord.Embed(
                                                                                color=color)
                                                                            logs.set_author(
                                                                                name="Aquhx msgs wizard")
                                                                            logs.description = "✅ Updated goodbye message."
                                                                            logs.set_footer(text="Aquhx msgs wizard",
                                                                                            icon_url=self.client.user.avatar_url)
                                                                            await sent.edit(embed=logs)
                                                                        await asyncio.sleep(3)
                                                                        em = discord.Embed(
                                                                            color=color)
                                                                        em.set_author(
                                                                            name="Aquhx msgs wizard")
                                                                        em.description = "✅ Completed all tasks, thank you for using Aquhx"
                                                                        em.set_footer(
                                                                            text="Aquhx msgs wizard", icon_url=self.client.user.avatar_url)
                                                                        await sent.edit(embed=em)
                                                                    except Exception as e:
                                                                        await ctx.send("{}" .format(e))
                                                            except Exception as e:
                                                                await ctx.send("{}".format(e))
                                                    except Exception as e:
                                                        await ctx.send("{}" .format(e))
                                            except asyncio.TimeoutError:
                                                await ctx.send("You took too long!")
                                    except Exception as e:
                                        await ctx.send("{}" .format(e))

                            except asyncio.TimeoutError:
                                await ID.delete()
                                logs = discord.Embed(color=color)
                                logs.set_author(name="Aquhx msgs wizard")
                                logs.description = "Would you like to continue without a welcome message set?. Y, N"
                                logs.set_footer(text="Aquhx msgs wizard",
                                                icon_url=self.client.user.avatar_url)
                                await sent.edit(embed=logs)
                                try:
                                    answer = await self.client.wait_for(
                                        'message',
                                        timeout=60.0,
                                        check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                                    if answer:
                                        try:
                                            await answer.delete()
                                            if answer.content == "Y" or 'y':
                                                em = discord.Embed(
                                                    color=color)
                                                em.set_author(
                                                    name="Aquhx msgs wizard")
                                                em.description = "✅ Completed all tasks, thank you for using Aquhx"
                                                em.set_footer(
                                                    text="Aquhx msgs wizard", icon_url=self.client.user.avatar_url)
                                                await sent.edit(embed=em)

                                            elif answer.content == "N" or 'n':
                                                await asyncio.sleep(3)
                                                logs = discord.Embed(
                                                    color=color)
                                                logs.set_author(
                                                    name="Aquhx msgs wizard")
                                                logs.description = "Next I require a welcome message."
                                                logs.set_footer(text="Aquhx msgs wizard",
                                                                icon_url=self.client.user.avatar_url)
                                                await sent.edit(embed=logs)
                                                try:
                                                    good = await self.client.wait_for(
                                                        'message',
                                                        timeout=60.0,
                                                        check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                                                    try:
                                                        msgs = good.content
                                                        await wel.delete()
                                                        res = await pg_con.fetchrow("SELECT msg FROM aquhx.welcome WHERE guild_id = $1", ctx.guild.id)
                                                        if res == None:
                                                            await pg_con.execute("INSERT INTO aquhx.welcome(guild_id, msg) VALUES($1, $2)", ctx.guild.id, msgs)
                                                            logs = discord.Embed(
                                                                color=color)
                                                            logs.set_author(
                                                                name="Aquhx msgs wizard")
                                                            logs.description = "✅ Set welcome message."
                                                            logs.set_footer(text="Aquhx msgs wizard",
                                                                            icon_url=self.client.user.avatar_url)
                                                        elif res != None:
                                                            await pg_con.execute("UPDATE aquhx.welcome SET msg = $1 WHERE guild_id = $2",   msgs, ctx.guild.id)
                                                            logs = discord.Embed(
                                                                color=color)
                                                            logs.set_author(
                                                                name="Aquhx msgs wizard")
                                                            logs.description = "✅ Updated welcome message."
                                                            logs.set_footer(text="Aquhx msgs wizard",
                                                                            icon_url=self.client.user.avatar_url)
                                                        await sent.edit(embed=logs)
                                                        await asyncio.sleep(3)
                                                        em = discord.Embed(
                                                            color=color)
                                                        em.set_author(
                                                            name="Aquhx msgs wizard")
                                                        em.description = "✅ Completed all tasks, thank you for using Aquhx"
                                                        em.set_footer(
                                                            text="Aquhx msgs wizard", icon_url=self.client.user.avatar_url)
                                                        await sent.edit(embed=em)
                                                    except Exception as e:
                                                        await ctx.send("{}" .format(e))
                                                except asyncio.TimeoutError:
                                                    await ctx.send("You never responded, terminating command..")
                                        except asyncio.TimeoutError:
                                            await ctx.send("You took too long !")
                                except asyncio.TimeoutError:
                                    await ctx.send("You took too long !")
                    except asyncio.TimeoutError:
                        await ctx.send("You took too long !")

                elif msg.content == "dellogs":
                    try:
                        result = await pg_con.fetchrow(f"SELECT * FROM aquhx.modlog WHERE guild_id = $1", ctx.guild.id)
                        if result is None:

                            em = discord.Embed(color=color,
                                               description="❌ You haven't configured a log channel!")

                        elif result is not None:

                            await pg_con.execute("DELETE FROM aquhx.modlog WHERE guild_id = $1", ctx.guild.id)
                            em = discord.Embed(color=color,
                                               description="✅ Removed the log channel from the database database!")
                        await sent.edit(embed=em)
                        await msg.delete()
                    except Exception as e:
                        await ctx.send("{}".format(e))

                elif msg.content == "delmsgs":
                    try:
                        await msg.delete()
                        res = await pg_con.fetchrow("SELECT channel_id FROM aquhx.messages WHERE guild_id = $1", ctx.guild.id)
                        if res == None:
                            em = discord.Embed(color=color)
                            em.description = "❌ You haven't configured a messages channel!"
                        elif res != None:
                            await pg_con.execute("DELETE FROM aquhx.messages WHERE guild_id = $1", ctx.guild.id)
                            em = discord.Embed(color=color,
                                               description="✅ Removed the messages channel from the database database!")
                        await sent.edit(embed=em)
                    except Exception as e:
                        await ctx.send("{}" .format(e))

                else:
                    await ctx.send("Not a valid argument")
        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send("[ERROR] You didn't respond in time", delete_after=10)
        finally:
            await pool.release(pg_con)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def prefix(self, ctx, prefix: str = None):
        if prefix == None:
            em = discord.Embed(color=color)
            em.title = "Prefix command"
            em.description = """
            INFO: [] = required, {} = optional
            Requires = Manage messages
            Arguments = [prefix]
            Description = Changes the prefix
            """
            em.set_footer(icon_url=ctx.author.avatar_url,
                          text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=em)
        elif prefix != None:
            try:
                if len(prefix) > 3:
                    await ctx.send("Can't have more than 3 letters")
                res = await self.client.db.fetchrow("SELECT prefix FROM aquhx.prefixes WHERE guild_id = $1", ctx.guild.id)
                if res != None:
                    await self.client.db.execute("UPDATE aquhx.prefixes SET prefix = $1 WHERE guild_id = $2", prefix, ctx.guild.id)
                    await ctx.send("Set")
                elif res == None:
                    await self.client.db.execute("INSERT INTO aquhx.prefixes(guild_id, prefix) VALUES($1, $2)", ctx.guild.id, "$")
                    await self.client.db.execute("UPDATE aquhx.prefixes SET prefix = $1 WHERE guild_id = $2", prefix, ctx.guild.id)
                    await ctx.send("Set")
            except Exception as e:
                await ctx.send("{}" .format(e))


def setup(client):
    client.add_cog(config(client))
