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

from discord.ext.commands import command, Cog, has_permissions
from discord import *
import asyncio
import time
color = 0xfffafa

class SetupClass(Cog):
    def __init__(self, client):
        self.t = time.localtime()
        self.cur = time.strftime("%I:%M %p", self.t)
        self.client = client
        self.check = "<a:greentick:825189056295862292>"
        self.fail = "<a:redX:825192396655427595>"

    @command()
    @has_permissions(manage_guild=True)
    async def setup(self, ctx):
        em = Embed(color=color)
        em.set_author(name=f"Cairo setup wizard",
                      icon_url=self.client.user.avatar_url)
        em.description = "Thanks for using Cairo, please respond to this message just by typing the name of the command like this\n```logs```\nor ignore the message"
        em.add_field(name="logs", value="Set up your logs")
        em.add_field(name="welcome", value="Set up the welcome message")
        em.add_field(name="goodbye", value="Set up the goodbye message")
        em.add_field(name="prefix", value="Change your guild prefix")
        em.add_field(
            name="welchan", value="Set the welcome channel")
        em.add_field(
            name="goodchan", value="Set the goodbye channel")
        em.add_field(name="remlogs",
                     value="Remove the logs channel from the database")
        em.add_field(
            name="remwel", value="Remove the welcome items from the database")
        em.add_field(name="remgood",
                     value="Remove the goodbye items from the database")
        em.set_footer(
            text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
        sent = await ctx.send(embed=em)
        try:
            msg = await self.client.wait_for(
                'message',
                timeout=60.0,
                check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
            if msg:
                if msg.content.casefold() == "logs":
                    await ctx.invoke(self.client.get_command("logs"))
                elif msg.content.casefold() == "welchan":
                    await ctx.invoke(self.client.get_command("welchan"))
                elif msg.content.casefold() == "goodchan":
                    await ctx.invoke(self.client.get_command("goodchan"))
                elif msg.content.casefold() == "welcome":
                    await ctx.invoke(self.client.get_command("welcome"))
                elif msg.content.casefold() == "goodbye":
                    await ctx.invoke(self.client.get_command("goodbye"))
                elif msg.content.casefold() == "prefix":
                    await ctx.invoke(self.client.get_command("prefix"))
                elif msg.content.casefold() == "remwel":
                    await ctx.invoke(self.client.get_command("remwel"))
                elif msg.content.casefold() == "remgood":
                    await ctx.invoke(self.client.get_command("remgood"))
                elif msg.content.casefold() == "remlogs":
                    await ctx.invoke(self.client.get_command("remlogs"))        
        except asyncio.TimeoutError:
            em = Embed(color=color)
            em.set_author(name="Cairo setup wizard",
                          icon_url=self.client.user.avatar_url)
            em.description = f"{self.fail} Sorry but you didn't respond in time!"
            em.set_footer(
                text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
            await sent.edit(embed=em)

    @command()
    @has_permissions(manage_messages=True)
    async def prefix(self, ctx, prefix: str = None):
        if prefix == None:
            em = Embed(color=color)
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
                self.client.cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = ?", (ctx.guild.id, ))
                res = self.client.cursor.fetchone()
                if res != None:
                    self.client.cursor.execute("UPDATE prefixes SET prefix = ? WHERE guild_id = ?", (prefix, ctx.guild.id, ))
                elif res == None:
                    self.client.cursor.execute("INSERT INTO prefixes(guild_id, prefix) VALUES(?, ?)", (ctx.guild.id, "$", ))
                    self.client.cursor.execute("UPDATE prefixes SET prefix = ? WHERE guild_id = ?", (prefix, ctx.guild.id, ))
                self.client.db.commit()
                em = Embed(color=color)
                em.description = f"{self.check} Set the prefix to {prefix}"
                await ctx.send(embed=em)
            except Exception as e:
                await ctx.send("{}".format(e))

    @command()
    @has_permissions(manage_guild=True)
    async def logs(self, ctx):
        em = Embed(color=self.client.color)
        em.set_author(name="Cairo setup",
                      icon_url="https://i.imgur.com/25uryCs.png")
        em.add_field(name="Please respond to this message\nwith a channel",
                     value="You have 1 minute to respond.\nYou can respond with a channel ID\n```82304050760096158```\nor by mentioning the channel")
        em.description = "If you don't respond in 1 minute the bot wont accept an answer"
        em.set_footer(text="Cairo setup",
                      icon_url="https://i.imgur.com/25uryCs.png")
        sent = await ctx.send(embed=em)
        try:
            msg = await self.client.wait_for(
                'message',
                timeout=60.0,
                check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
            if msg:
                await msg.delete()
                ID = msg.content
                new = str(ID)
                x = new.replace("<#", "")
                y = x.replace(">", "")
                em = Embed(color=color)
                em.set_author(name="Cairo setup",
                              icon_url="https://i.imgur.com/25uryCs.png")
                em.add_field(name=f"{self.client.complete} Thanks for responding",
                             value=f"I set your logging channel to ``{y}``")
                em.set_footer(
                    text=f"Cairo setup | Requested by {ctx.author.name}", icon_url="https://i.imgur.com/25uryCs.png")
                await sent.edit(embed=em)
                self.client.cursor.execute(
                    "SELECT channel_id FROM modlog WHERE guild_id = ?", (ctx.guild.id,))
                result = self.client.cursor.fetchone()
                if result == None:
                    self.client.cursor.execute(
                        "INSERT INTO modlog (guild_id, channel_id) VALUES (?, ?)", (ctx.guild.id, int(y),))
                elif result != None:
                    self.client.cursor.execute(
                        "UPDATE modlog SET channel_id = ? WHERE guild_id = ?", (int(y), ctx.guild.id, ))
                self.client.db.commit()
        except asyncio.TimeoutError:
            em = Embed(color=self.client.color)
            em.set_author(name="Cairo setup",
                          icon_url="https://i.imgur.com/25uryCs.png")
            em.add_field(name=f"{self.client.fail} You never responded!",
                         value="You didn't respond in 1 minute!")
            em.set_footer(text="Cairo setup",
                          icon_url="https://i.imgur.com/25uryCs.png")
            await sent.edit(embed=em)

    @command()
    @has_permissions(manage_guild=True)
    async def welcome(self, ctx):
        em = Embed(color=self.client.color)
        em.set_author(name="Cairo setup",
                      icon_url="https://i.imgur.com/25uryCs.png")
        em.add_field(name="Please respond to this message\nwith a message",
                     value="You have 1 minute to respond.\nYou can respond with any message")
        em.description = "If you don't respond in 1 minute the bot wont accept an answer\n**Valid arguments**\n\n```{user} - Member's name\n{mention} - Mention the user\n{members} - Amount of users in guild\n{guild} - guild name\nOther valid arguments are discord.py\narguments for the on_member_join event```"
        em.set_footer(text="Cairo setup",
                      icon_url="https://i.imgur.com/25uryCs.png")
        sent = await ctx.send(embed=em)
        try:
            msg = await self.client.wait_for(
                'message',
                timeout=60.0,
                check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
            if msg:
                await msg.delete()
                em = Embed(color=color)
                em.set_author(name="Cairo setup",
                              icon_url="https://i.imgur.com/25uryCs.png")
                em.add_field(name=f"{self.client.complete} Thanks for responding",
                             value=f"I set your welcome message to\n**{msg.content}**")
                em.set_footer(
                    text=f"Cairo setup | Requested by {ctx.author.name}", icon_url="https://i.imgur.com/25uryCs.png")
                await sent.edit(embed=em)
                self.client.cursor.execute(
                    "SELECT welcome FROM welcome WHERE guild_id = ?", (ctx.guild.id, ))
                result = self.client.cursor.fetchone()
                if result == None:
                    self.client.cursor.execute(
                        "INSERT INTO welcome (guild_id, welcome) VALUES (?, ?)", (ctx.guild.id, msg.content, ))
                elif result != None:
                    self.client.cursor.execute(
                        "UPDATE welcome SET welcome = ? WHERE guild_id = ?", (msg.content, ctx.guild.id,))
                self.client.db.commit()
        except asyncio.TimeoutError:
            em = Embed(color=self.client.color)
            em.set_author(name="Cairo setup",
                          icon_url="https://i.imgur.com/25uryCs.png")
            em.add_field(name=f"{self.client.fail} You never responded!",
                         value="You didn't respond in 1 minute!")
            em.set_footer(text="Cairo setup",
                          icon_url="https://i.imgur.com/25uryCs.png")
            await sent.edit(embed=em)

    @command()
    @has_permissions(manage_guild=True)
    async def goodbye(self, ctx):
        em = Embed(color=self.client.color)
        em.set_author(name="Cairo setup",
                      icon_url="https://i.imgur.com/25uryCs.png")
        em.add_field(name="Please respond to this message\nwith a message",
                     value="You have 1 minute to respond.\nYou can respond with any message")
        em.description = "If you don't respond in 1 minute the bot wont accept an answer\n**Valid arguments**\n\n```{user} - Member's name\n{mention} - Mention the user\n{members} - Amount of users in guild\n{guild} - guild name\nOther valid arguments are discord.py\narguments for the on_member_join event```"
        em.set_footer(text="Cairo setup",
                      icon_url="https://i.imgur.com/25uryCs.png")
        sent = await ctx.send(embed=em)
        try:
            msg = await self.client.wait_for(
                'message',
                timeout=60.0,
                check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
            if msg:
                await msg.delete()
                em = Embed(color=color)
                em.set_author(name="Cairo setup",
                              icon_url="https://i.imgur.com/25uryCs.png")
                em.add_field(name=f"{self.client.complete} Thanks for responding",
                             value=f"I set your goodbye message to\n**{msg.content}**")
                em.set_footer(
                    text=f"Cairo setup | Requested by {ctx.author.name}", icon_url="https://i.imgur.com/25uryCs.png")
                await sent.edit(embed=em)
                self.client.cursor.execute(
                    "SELECT goodbye FROM goodbye WHERE guild_id = ?", (ctx.guild.id, ))
                result = self.client.cursor.fetchone()
                if result == None:
                    self.client.cursor.execute(
                        "INSERT INTO goodbye (guild_id, goodbye) VALUES (?, ?)", (ctx.guild.id, msg.content, ))
                elif result != None:
                    self.client.cursor.execute(
                        "UPDATE goodbye SET goodbye = ? WHERE guild_id = ?", (msg.content, ctx.guild.id,))
                self.client.db.commit()
        except asyncio.TimeoutError:
            em = Embed(color=self.client.color)
            em.set_author(name="Cairo setup",
                          icon_url="https://i.imgur.com/25uryCs.png")
            em.add_field(name=f"{self.client.fail} You never responded!",
                         value="You didn't respond in 1 minute!")
            em.set_footer(text="Cairo setup",
                          icon_url="https://i.imgur.com/25uryCs.png")
            await sent.edit(embed=em)


    @command()
    @has_permissions(manage_guild=True)
    async def welchan(self, ctx):
        em = Embed(color=self.client.color)
        em.set_author(name="Cairo setup",
                      icon_url="https://i.imgur.com/25uryCs.png")
        em.add_field(name="Please respond to this message\nwith a channel",
                     value="You have 1 minute to respond.\nYou can respond with a channel ID\n```82304050760096158```\nor by mentioning the channel")
        em.description = "If you don't respond in 1 minute the bot wont accept an answer"
        em.set_footer(text="Cairo setup",
                      icon_url="https://i.imgur.com/25uryCs.png")
        sent = await ctx.send(embed=em)
        try:
            msg = await self.client.wait_for(
                'message',
                timeout=60.0,
                check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
            if msg:
                await msg.delete()
                ID = msg.content
                new = str(ID)
                x = new.replace("<#", "")
                y = x.replace(">", "")
                em = Embed(color=color)
                em.set_author(name="Cairo setup",
                              icon_url="https://i.imgur.com/25uryCs.png")
                em.add_field(name=f"{self.client.complete} Thanks for responding",
                             value=f"I set your welcome channel channel to ``{y}``")
                em.set_footer(
                    text=f"Cairo setup | Requested by {ctx.author.name}", icon_url="https://i.imgur.com/25uryCs.png")
                await sent.edit(embed=em)
                self.client.cursor.execute(
                    "SELECT welchan FROM welcome WHERE guild_id = ?", (ctx.guild.id,))
                result = self.client.cursor.fetchone()
                if result == None:
                    self.client.cursor.execute(
                        "INSERT INTO welcome (guild_id, welchan) VALUES (?, ?)", (ctx.guild.id, int(y),))
                elif result != None:
                    self.client.cursor.execute(
                        "UPDATE welcome SET welchan = ? WHERE guild_id = ?", (int(y), ctx.guild.id, ))
                self.client.db.commit()
        except asyncio.TimeoutError:
            em = Embed(color=self.client.color)
            em.set_author(name="Cairo setup",
                          icon_url="https://i.imgur.com/25uryCs.png")
            em.add_field(name=f"{self.client.fail} You never responded!",
                         value="You didn't respond in 1 minute!")
            em.set_footer(text="Cairo setup",
                          icon_url="https://i.imgur.com/25uryCs.png")
            await sent.edit(embed=em)

    @command()
    @has_permissions(manage_guild=True)
    async def goodchan(self, ctx):
        em = Embed(color=self.client.color)
        em.set_author(name="Cairo setup",
                      icon_url="https://i.imgur.com/25uryCs.png")
        em.add_field(name="Please respond to this message\nwith a channel",
                     value="You have 1 minute to respond.\nYou can respond with a channel ID\n```82304050760096158```\nor by mentioning the channel")
        em.description = "If you don't respond in 1 minute the bot wont accept an answer"
        em.set_footer(text="Cairo setup",
                      icon_url="https://i.imgur.com/25uryCs.png")
        sent = await ctx.send(embed=em)
        try:
            msg = await self.client.wait_for(
                'message',
                timeout=60.0,
                check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
            if msg:
                await msg.delete()
                ID = msg.content
                new = str(ID)
                x = new.replace("<#", "")
                y = x.replace(">", "")
                em = Embed(color=color)
                em.set_author(name="Cairo setup",
                              icon_url="https://i.imgur.com/25uryCs.png")
                em.add_field(name=f"{self.client.complete} Thanks for responding",
                             value=f"I set your goodbye channel channel to ``{y}``")
                em.set_footer(
                    text=f"Cairo setup | Requested by {ctx.author.name}", icon_url="https://i.imgur.com/25uryCs.png")
                await sent.edit(embed=em)
                self.client.cursor.execute(
                    "SELECT goodchan FROM goodbye WHERE guild_id = ?", (ctx.guild.id,))
                result = self.client.cursor.fetchone()
                if result == None:
                    self.client.cursor.execute(
                        "INSERT INTO goodbye (guild_id, goodchan) VALUES (?, ?)", (ctx.guild.id, int(y),))
                elif result != None:
                    self.client.cursor.execute(
                        "UPDATE goodbye SET goodchan = ? WHERE guild_id = ?", (int(y), ctx.guild.id, ))
                self.client.db.commit()
        except asyncio.TimeoutError:
            em = Embed(color=self.client.color)
            em.set_author(name="Cairo setup",
                          icon_url="https://i.imgur.com/25uryCs.png")
            em.add_field(name=f"{self.client.fail} You never responded!",
                         value="You didn't respond in 1 minute!")
            em.set_footer(text="Cairo setup",
                          icon_url="https://i.imgur.com/25uryCs.png")
            await sent.edit(embed=em)


    @command()
    @has_permissions(manage_guild=True)
    async def remwel(self, ctx):
        self.client.cursor.execute("SELECT welcome, welchan FROM welcome WHERE guild_id = ?", (ctx.guild.id,))
        result = self.client.cursor.fetchone()
        if result == None:
            em = Embed(color=self.client.color)
            em.set_author(name="Cairo setup",
                      icon_url="https://i.imgur.com/25uryCs.png")
            em.add_field(name=f"{self.client.fail} Oops!", value="You don't have any welcome items in the database")
            em.set_footer(
                    text=f"Cairo setup | Requested by {ctx.author.name}", icon_url="https://i.imgur.com/25uryCs.png")
            await ctx.send(embed=em)
        elif result != None:
            self.client.cursor.execute("DELETE FROM welcome WHERE guild_id = ?", (ctx.guild.id,))
            em = Embed(color=self.client.color)
            em.set_author(name="Cairo setup",
                          icon_url="https://i.imgur.com/25uryCs.png")
            em.add_field(name=f"{self.client.complete} Deleted!",
                         value="I removed your welcome items from the database!")
            em.set_footer(
                text=f"Cairo setup | Requested by {ctx.author.name}", icon_url="https://i.imgur.com/25uryCs.png")
            await ctx.send(embed=em)
            self.client.db.commit()

    @command()
    @has_permissions(manage_guild=True)
    async def remgood(self, ctx):
        self.client.cursor.execute(
            "SELECT goodbye, goodchan FROM goodbye WHERE guild_id = ?", (ctx.guild.id,))
        result = self.client.cursor.fetchone()
        if result == None:
            em = Embed(color=self.client.color)
            em.set_author(name="Cairo setup",
                          icon_url="https://i.imgur.com/25uryCs.png")
            em.add_field(name=f"{self.client.fail} Oops!",
                         value="You don't have any goodbye items in the database")
            em.set_footer(
                text=f"Cairo setup | Requested by {ctx.author.name}", icon_url="https://i.imgur.com/25uryCs.png")
            await ctx.send(embed=em)
        elif result != None:
            self.client.cursor.execute(
                "DELETE FROM goodbye WHERE guild_id = ?", (ctx.guild.id,))
            em = Embed(color=self.client.color)
            em.set_author(name="Cairo setup",
                          icon_url="https://i.imgur.com/25uryCs.png")
            em.add_field(name=f"{self.client.complete} Deleted!",
                         value="I removed your goodbye items from the database!")
            em.set_footer(
                text=f"Cairo setup | Requested by {ctx.author.name}", icon_url="https://i.imgur.com/25uryCs.png")
            await ctx.send(embed=em)
            self.client.db.commit()


    @command()
    @has_permissions(manage_guild=True)
    async def remlogs(self, ctx):
        self.client.cursor.execute(
            "SELECT * FROM modlog WHERE guild_id = ?", (ctx.guild.id,))
        result = self.client.cursor.fetchone()
        if result == None:
            em = Embed(color=self.client.color)
            em.set_author(name="Cairo setup",
                          icon_url="https://i.imgur.com/25uryCs.png")
            em.add_field(name=f"{self.client.fail} Oops!",
                         value="You don't have a log channel in the database")
            em.set_footer(
                text=f"Cairo setup | Requested by {ctx.author.name}", icon_url="https://i.imgur.com/25uryCs.png")
            await ctx.send(embed=em)
        elif result != None:
            self.client.cursor.execute(
                "DELETE FROM modlog WHERE guild_id = ?", (ctx.guild.id,))
            em = Embed(color=self.client.color)
            em.set_author(name="Cairo setup",
                          icon_url="https://i.imgur.com/25uryCs.png")
            em.add_field(name=f"{self.client.complete} Deleted!",
                         value="I removed your log channel from the database!")
            em.set_footer(
                text=f"Cairo setup | Requested by {ctx.author.name}", icon_url="https://i.imgur.com/25uryCs.png")
            await ctx.send(embed=em)
            self.client.db.commit()


def setup(client):
    client.add_cog(SetupClass(client))
