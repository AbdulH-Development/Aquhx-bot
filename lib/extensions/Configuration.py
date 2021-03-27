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
        em.set_author(name="Cairo setup wizard")
        em.description = """
        Welcome to the Cairo setup wizard,
        please select a channel to setup by using the name.
        **logs** : Configure your log channel.
        **addmsgs** : Configure your welcome/goodbye messages and channel.
        **dellogs** : Remove the log channel from the database.
        **delmsgs** : Remove the welcome/goodbye channel and messages from the database.
        """
        em.set_footer(text="Cairo setup wizard",
                      icon_url=self.client.user.avatar_url)
        sent = await ctx.send(embed=em)

        try:
            msg = await self.client.wait_for(
                'message',
                timeout=60.0,
                check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
            if msg:
                if msg.content == "logs":
                    logs = discord.Embed(color=color)
                    logs.set_author(name="Cairo log wizard")
                    logs.description = "Welcome to the log wizard,\nplease provide me with a channel ID\nExample. 818598634823090197 <- if you try to use that it won't work for you."
                    logs.set_footer(text="Cairo log wizard",
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
                                res = await self.client.db.fetchrow("SELECT channel_id FROM db.modlog WHERE guild_id = $1", ctx.guild.id)
                                if res == None:
                                    await self.client.db.execute("INSERT INTO db.modlog(guild_id, channel_id) VALUES($1, $2)", ctx.guild.id, int(log))
                                    em = discord.Embed(color=color,
                                                       description="✅ Set logs channel!")
                                    await sent.edit(embed=em)
                                elif res != None:
                                    await self.client.db.execute("UPDATE db.modlog SET channel_id = $1 WHERE guild_id = $2", int(log), ctx.guild.id)
                                    em = discord.Embed(color=color,
                                                       description="✅ Updated logs channel!")
                                    await sent.edit(embed=em)
                            except Exception as e:
                                await ctx.send("{}".format(e))
                    except asyncio.TimeoutError:
                        await ctx.send("Took too long!")

                elif msg.content == "addmsgs":
                    logs = discord.Embed(color=color)
                    logs.set_author(name="Cairo msgs wizard")
                    logs.description = "Welcome to the msgs wizard,\nplease provide me with a channel ID\nExample. 818598634823090197 <- if you try to use that it won't work for you."
                    logs.set_footer(text="Cairo msgs wizard",
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
                            res = await self.client.db.fetchrow("SELECT channel_id FROM db.messages WHERE guild_id = $1", ctx.guild.id)
                            if res == None:
                                await self.client.db.execute("INSERT INTO db.messages(guild_id, channel_id) VALUES($1, $2)", ctx.guild.id, int(n))
                                em = discord.Embed(color=color)
                                em.set_author(name="Cairo msgs wizard")
                                em.description = "✅ Set the message channel"
                                em.set_footer(
                                    text="Cairo msgs wizard", icon_url=self.client.user.avatar_url)
                            elif res != None:
                                await self.client.db.execute("UPDATE db.messages SET channel_id = $1 WHERE guild_id = $2", int(n), ctx.guild.id)
                                em = discord.Embed(color=color)
                                em.set_author(name="Cairo msgs wizard")
                                em.description = "✅ Set the message channel"
                                em.set_footer(
                                    text="Cairo msgs wizard", icon_url=self.client.user.avatar_url)
                            await sent.edit(embed=em)
                            await asyncio.sleep(3)
                            logs = discord.Embed(color=color)
                            logs.set_author(name="Cairo msgs wizard")
                            logs.description = "Next I require a welcome message."
                            logs.set_footer(text="Cairo msgs wizard",
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
                                        res = await self.client.db.fetchrow("SELECT msg FROM db.welcome WHERE guild_id = $1", ctx.guild.id)
                                        if res == None:
                                            await self.client.db.execute("INSERT INTO db.welcome(guild_id, msg) VALUES($1, $2)", ctx.guild.id, msgs)
                                            logs = discord.Embed(color=color)
                                            logs.set_author(
                                                name="Cairo msgs wizard")
                                            logs.description = "✅ Set the welcome message!"
                                            logs.set_footer(text="Cairo msgs wizard",
                                                            icon_url=self.client.user.avatar_url)
                                            await sent.edit(embed=logs)
                                        elif res != None:
                                            await self.client.db.execute("UPDATE db.welcome SET msg = $1 WHERE guild_id = $2", msgs, ctx.guild.id)
                                            logs = discord.Embed(color=color)
                                            logs.set_author(
                                                name="Cairo msgs wizard")
                                            logs.description = "✅ Updated the welcome message!"
                                            logs.set_footer(text="Cairo msgs wizard",
                                                            icon_url=self.client.user.avatar_url)
                                            await sent.edit(embed=logs)
                                        await asyncio.sleep(3)
                                        logs = discord.Embed(color=color)
                                        logs.set_author(
                                            name="Cairo msgs wizard")
                                        logs.description = "Next I require a goodbye message."
                                        logs.set_footer(text="Cairo msgs wizard",
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
                                                    res = await self.client.db.fetchrow("SELECT msg FROM db.goodbye WHERE guild_id = $1", ctx.guild.id)
                                                    if res == None:
                                                        await self.client.db.execute("INSERT INTO db.goodbye(guild_id, msg) VALUES($1, $2)", ctx.guild.id, msgs)
                                                        logs = discord.Embed(
                                                            color=color)
                                                        logs.set_author(
                                                            name="Cairo msgs wizard")
                                                        logs.description = "✅ Set goodbye message."
                                                        logs.set_footer(text="Cairo msgs wizard",
                                                                        icon_url=self.client.user.avatar_url)
                                                        await sent.edit(embed=logs)
                                                    elif res != None:
                                                        await self.client.db.execute("UPDATE db.goodbye SET msg = $1 WHERE guild_id = $2", msgs, ctx.guild.id)
                                                        logs = discord.Embed(
                                                            color=color)
                                                        logs.set_author(
                                                            name="Cairo msgs wizard")
                                                        logs.description = "✅ Updated goodbye message."
                                                        logs.set_footer(text="Cairo msgs wizard",
                                                                        icon_url=self.client.user.avatar_url)
                                                        await sent.edit(embed=logs)
                                                    await asyncio.sleep(3)
                                                    em = discord.Embed(
                                                        color=color)
                                                    em.set_author(
                                                        name="Cairo msgs wizard")
                                                    em.description = "✅ Completed all tasks, thank you for using Cairo"
                                                    em.set_footer(
                                                        text="Cairo msgs wizard", icon_url=self.client.user.avatar_url)
                                                    await sent.edit(embed=em)
                                                except Exception as e:
                                                    await ctx.send("{}" .format(e))
                                        except asyncio.TimeoutError:
                                            logs = discord.Embed(color=color)
                                            logs.set_author(
                                                name="Cairo msgs wizard")
                                            logs.description = "Do you want to continue without a goodbye message? Y, N"
                                            logs.set_footer(text="Cairo msgs wizard",
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
                                                                name="Cairo msgs wizard")
                                                            em.description = "✅ Completed all tasks, thank you for using Cairo"
                                                            em.set_footer(
                                                                text="Cairo msgs wizard", icon_url=self.client.user.avatar_url)
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
                                                                        res = await self.client.db.fetchrow("SELECT msg FROM db.goodbye WHERE guild_id = $1", ctx.guild.id)
                                                                        if res == None:
                                                                            await self.client.db.execute("INSERT INTO db.goodbye(guild_id, msg) VALUES($1, $2)", ctx.guild.id, msgs)
                                                                            logs = discord.Embed(
                                                                                color=color)
                                                                            logs.set_author(
                                                                                name="Cairo msgs wizard")
                                                                            logs.description = "✅ Set goodbye message."
                                                                            logs.set_footer(text="Cairo msgs wizard",
                                                                                            icon_url=self.client.user.avatar_url)
                                                                            await sent.edit(embed=logs)
                                                                        elif res != None:
                                                                            await self.client.db.execute("UPDATE db.goodbye SET msg = $1 WHERE guild_id = $2", msgs, ctx.guild.id)
                                                                            logs = discord.Embed(
                                                                                color=color)
                                                                            logs.set_author(
                                                                                name="Cairo msgs wizard")
                                                                            logs.description = "✅ Updated goodbye message."
                                                                            logs.set_footer(text="Cairo msgs wizard",
                                                                                            icon_url=self.client.user.avatar_url)
                                                                            await sent.edit(embed=logs)
                                                                        await asyncio.sleep(3)
                                                                        em = discord.Embed(
                                                                            color=color)
                                                                        em.set_author(
                                                                            name="Cairo msgs wizard")
                                                                        em.description = "✅ Completed all tasks, thank you for using Cairo"
                                                                        em.set_footer(
                                                                            text="Cairo msgs wizard", icon_url=self.client.user.avatar_url)
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
                                logs = discord.Embed(color=color)
                                logs.set_author(
                                    name="Cairo msgs wizard")
                                logs.description = "Would you like to continue without a welcome message set?. Y, N"
                                logs.set_footer(text="Cairo msgs wizard",
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
                                                logs = discord.Embed(
                                                    color=color)
                                                logs.set_author(
                                                    name="Cairo msgs wizard")
                                                logs.description = "Next I require a goodbye message."
                                                logs.set_footer(text="Cairo msgs wizard",
                                                                icon_url=self.client.user.avatar_url)
                                                await sent.edit(embed=logs)
                                                try:
                                                    good = await self.client.wait_for(
                                                        'message',
                                                        timeout=60.0,
                                                        check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                                                    try:
                                                        msgs = good.content
                                                        res = await self.client.db.fetchrow("SELECT msg FROM db.goodbye WHERE guild_id = $1", ctx.guild.id)
                                                        if res == None:
                                                            await self.client.db.execute("INSERT INTO db.goodbye(guild_id, msg) VALUES($1, $2)", ctx.guild.id, msgs)
                                                            logs = discord.Embed(
                                                                color=color)
                                                            logs.set_author(
                                                                name="Cairo msgs wizard")
                                                            logs.description = "✅ Set goodbye message."
                                                            logs.set_footer(text="Cairo msgs wizard",
                                                                            icon_url=self.client.user.avatar_url)
                                                        elif res != None:
                                                            await self.client.db.execute("UPDATE db.goodbye SET msg = $1 WHERE guild_id = $2",   msgs, ctx.guild.id)
                                                            logs = discord.Embed(
                                                                color=color)
                                                            logs.set_author(
                                                                name="Cairo msgs wizard")
                                                            logs.description = "✅ Updated goodbye message."
                                                            logs.set_footer(text="Cairo msgs wizard",
                                                                            icon_url=self.client.user.avatar_url)
                                                        await sent.edit(embed=logs)
                                                        await good.delete()
                                                        await asyncio.sleep(3)
                                                        em = discord.Embed(
                                                            color=color)
                                                        em.set_author(
                                                            name="Cairo msgs wizard")
                                                        em.description = "✅ Completed all tasks, thank you for using Cairo"
                                                        em.set_footer(
                                                            text="Cairo msgs wizard", icon_url=self.client.user.avatar_url)
                                                        await sent.edit(embed=em)
                                                    except Exception as e:
                                                        await ctx.send("{}".format(e))
                                                except asyncio.TimeoutError:
                                                    await ctx.send("You took too long!")

                                            elif answer.content == "N" or 'n':
                                                await asyncio.sleep(3)
                                                logs = discord.Embed(
                                                    color=color)
                                                logs.set_author(
                                                    name="Cairo msgs wizard")
                                                logs.description = "Next I require a welcome message."
                                                logs.set_footer(text="Cairo msgs wizard",
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
                                                            res = await self.client.db.fetchrow("SELECT msg FROM db.welcome WHERE guild_id = $1", ctx.guild.id)
                                                            if res == None:
                                                                await self.client.db.execute("INSERT INTO db.welcome(guild_id, msg) VALUES($1, $2)", ctx.guild.id, msgs)
                                                            elif res != None:
                                                                await self.client.db.execute("UPDATE db.welcome SET msg = $1 WHERE guild_id = $2",   msgs, ctx.guild.id)
                                                                logs = discord.Embed(
                                                                    color=color)
                                                                logs.set_author(
                                                                    name="Cairo msgs wizard")
                                                                logs.description = "✅ Updated welcome message."
                                                                logs.set_footer(text="Cairo msgs wizard",
                                                                                icon_url=self.client.user.avatar_url)
                                                            await sent.edit(embed=logs)
                                                            await good.delete()
                                                            await asyncio.sleep(3)
                                                            logs = discord.Embed(
                                                                color=color)
                                                            logs.set_author(
                                                                name="Cairo msgs wizard")
                                                            logs.description = "Next I require a welcome message."
                                                            logs.set_footer(text="Cairo msgs wizard",
                                                                            icon_url=self.client.user.avatar_url)
                                                            await sent.edit(embed=logs)
                                                            try:
                                                                await good.delete()
                                                                good = await self.client.wait_for(
                                                                    'message',
                                                                    timeout=60.0,
                                                                    check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                                                                res = await self.client.db.fetchrow("SELECT msg FROM db.goodbye WHERE guild_id = $1", ctx.guild.id)
                                                                if res == None:
                                                                    await self.client.db.execute("INSERT INTO db.goodbye(guild_id, msg) VALUES($1, $2)", ctx.guild.id, msgs)
                                                                    logs = discord.Embed(
                                                                        color=color)
                                                                    logs.set_author(
                                                                        name="Cairo msgs wizard")
                                                                    logs.description = "✅ Set goodbye message."
                                                                    logs.set_footer(text="Cairo msgs wizard",
                                                                                    icon_url=self.client.user.avatar_url)
                                                                    await sent.edit(embed=logs)
                                                                elif res != None:
                                                                    await self.client.db.execute("UPDATE db.goodbye SET msg = $1 WHERE guild_id = $2", msgs, ctx.guild.id)
                                                                    logs = discord.Embed(
                                                                        color=color)
                                                                    logs.set_author(
                                                                        name="Cairo msgs wizard")
                                                                    logs.description = "✅ Updated goodbye message."
                                                                    logs.set_footer(text="Cairo msgs wizard",
                                                                                    icon_url=self.client.user.avatar_url)
                                                                    await sent.edit(embed=logs)
                                                                    await asyncio.sleep(3)
                                                                    em = discord.Embed(
                                                                        color=color)
                                                                    em.set_author(
                                                                        name="Cairo msgs wizard")
                                                                    em.description = "✅ Completed all tasks, thank you for using Cairo"
                                                                    em.set_footer(
                                                                        text="Cairo msgs wizard", icon_url=self.client.user.avatar_url)
                                                                await sent.edit(embed=em)
                                                            except asyncio.TimeoutError:
                                                                await ctx.send("You didn't respond in time")
                                                        except Exception as e:
                                                            await ctx.send("{}".format(e))
                                                except Exception as e:
                                                    await ctx.send("{}".format(e))
                                        except Exception as e:
                                            await ctx.send("{}" .format(e))
                                except asyncio.TimeoutError:
                                    await ctx.send("You took too long!")
                    except asyncio.TimeoutError:
                        await ctx.send("You took too long!")

                elif msg.content == "dellogs":
                    try:
                        result = await self.client.db.fetchrow(f"SELECT * FROM db.modlog WHERE guild_id = $1", ctx.guild.id)
                        if result is None:

                            em = discord.Embed(color=color,
                                               description="❌ You haven't configured a log channel!")

                        elif result is not None:

                            await self.client.db.execute("DELETE FROM db.modlog WHERE guild_id = $1", ctx.guild.id)
                            em = discord.Embed(color=color,
                                               description="✅ Removed the log channel from the database!")
                        await sent.edit(embed=em)
                        await msg.delete()
                    except Exception as e:
                        await ctx.send("{}".format(e))

                elif msg.content == "delmsgs":
                    try:
                        await msg.delete()
                        res = await self.client.db.fetchrow("SELECT channel_id FROM db.messages WHERE guild_id = $1", ctx.guild.id)
                        if res == None:
                            em = discord.Embed(color=color)
                            em.description = "❌ You haven't configured a messages channel!"
                        elif res != None:
                            await self.client.db.execute("DELETE FROM db.messages WHERE guild_id = $1", ctx.guild.id)
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
                res = await self.client.db.fetchrow("SELECT prefix FROM db.prefixes WHERE guild_id = $1", ctx.guild.id)
                if res != None:
                    await self.client.db.execute("UPDATE db.prefixes SET prefix = $1 WHERE guild_id = $2", prefix, ctx.guild.id)
                    await ctx.send("Set")
                elif res == None:
                    await self.client.db.execute("INSERT INTO db.prefixes(guild_id, prefix) VALUES($1, $2)", ctx.guild.id, "$")
                    await self.client.db.execute("UPDATE db.prefixes SET prefix = $1 WHERE guild_id = $2", prefix, ctx.guild.id)
                    await ctx.send("Set")
            except Exception as e:
                await ctx.send("{}" .format(e))


def setup(client):
    client.add_cog(config(client))
