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
from ..bot import color
from ..bot import dbinfo
from discord import *
import asyncio
import time


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
                    await msg.delete()
                    em = Embed(color=color)
                    em.set_author(name="Cairo setup wizard",
                                  icon_url=self.client.user.avatar_url)
                    em.description = "Thanks for responding to the message, please respond by\nA). Mentioning a channel\nB). Giving me a channel ID"
                    em.add_field(name="Example of how to respond",
                                 value="```<#796866034534580264>``` or ```796866034534580264```")
                    em.set_footer(
                        text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                    await sent.edit(embed=em)
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
                            em.set_author(name="Cairo setup wizard",
                                          icon_url=self.client.user.avatar_url)
                            em.description = f"I set the ID to ``{y}``"
                            em.add_field(name=f"{self.check} Thank your for using Cairo setup wizard!",
                                         value=f"I have finished all my tasks!")
                            em.set_footer(
                                text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                            await sent.edit(embed=em)
                            result = await self.client.db.fetchrow("SELECT channel_id FROM db.modlog WHERE guild_id = $1", ctx.guild.id)
                            if result == None:
                                await self.client.db.execute("INSERT INTO db.modlog(guild_id, channel_id) VALUES($1, $2)", ctx.guild.id, int(y))
                            elif result != None:
                                await self.client.db.execute("UPDATE db.modlog SET channel_id = $1 WHERE guild_id = $2", int(y), ctx.guild.id)
                    except asyncio.TimeoutError:
                        em = Embed(color=color)
                        em.set_author(name="Cairo setup wizard",
                                      icon_url=self.client.user.avatar_url)
                        em.description = f"{self.fail} Sorry but you didn't respond in time!"
                        em.set_footer(
                            text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                        await sent.edit(embed=em)

                elif msg.content.casefold() == "goodbye":
                    await msg.delete()
                    em = Embed(color=color)
                    em.set_author(name="Cairo setup wizard",
                                  icon_url=self.client.user.avatar_url)
                    em.description = "Thanks for responding to the message, please respond by\ngiving me a goodbye message"
                    em.add_field(
                        name="Parameters", value="```{mention} - mention the member\n{members} - # of guild members\n{user} - the member name```")
                    em.set_footer(
                        text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                    await sent.edit(embed=em)
                    try:
                        msg = await self.client.wait_for(
                            'message',
                            timeout=60.0,
                            check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                        if msg:
                            await msg.delete()
                            em = Embed(color=color)
                            em.set_author(name="Cairo setup wizard",
                                          icon_url=self.client.user.avatar_url)
                            em.description = f"Set the goodbye message to\n```{msg.content}```"
                            em.add_field(name=f"{self.check} Thank your for using Cairo setup wizard!",
                                         value=f"I have finished all my tasks!")
                            em.set_footer(
                                text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                            await sent.edit(embed=em)
                            result = await self.client.db.fetchrow("SELECT msg FROM db.goodbye WHERE guild_id = $1", ctx.guild.id)
                            if result == None:
                                await self.client.db.execute("INSERT INTO db.goodbye(guild_id, msg) VALUES($1, $2)", ctx.guild.id, str(msg.content))
                            elif result != None:
                                await self.client.db.execute("UPDATE db.goodbye SET msg = $1 WHERE guild_id = $2", str(msg.content), ctx.guild.id)
                    except asyncio.TimeoutError:
                        em = Embed(color=color)
                        em.set_author(name="Cairo setup wizard",
                                      icon_url=self.client.user.avatar_url)
                        em.description = f"{self.fail} Sorry but you didn't respond in time!"
                        em.set_footer(
                            text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                        await sent.edit(embed=em)
                elif msg.content.casefold() == "welcome":
                    await msg.delete()
                    em = Embed(color=color)
                    em.set_author(name="Cairo setup wizard",
                                  icon_url=self.client.user.avatar_url)
                    em.description = "Thanks for responding to the message, please respond by\ngiving me a welcome message"
                    em.add_field(
                        name="Parameters", value="```{mention} - mention the member\n{members} - # of guild members\n{user} - the member name```")
                    em.set_footer(
                        text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                    await sent.edit(embed=em)
                    try:
                        msg = await self.client.wait_for(
                            'message',
                            timeout=60.0,
                            check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                        if msg:
                            try:
                                await msg.delete()
                                em = Embed(color=color)
                                em.set_author(name="Cairo setup wizard",
                                          icon_url=self.client.user.avatar_url)
                                em.description = f"Set the welcome message to\n```{msg.content}```"
                                em.add_field(name=f"{self.check} Thank your for using Cairo setup wizard!",
                                         value=f"I have finished all my tasks!")
                                em.set_footer(
                                    text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                                await sent.edit(embed=em)
                                result = await self.client.db.fetchrow("SELECT msg FROM db.welcome WHERE guild_id = $1", ctx.guild.id)
                                if result == None:
                                    await self.client.db.execute("INSERT INTO db.welcome(guild_id, msg) VALUES($1, $2)", ctx.guild.id, str(msg.content))
                                elif result != None:
                                    await self.client.db.execute("UPDATE db.welcome SET msg = $1 WHERE guild_id = $2", str(msg.content), ctx.guild.id)
                            except Exception as e:
                                print(e)
                    except asyncio.TimeoutError:
                        em = Embed(color=color)
                        em.set_author(name="Cairo setup wizard",
                                      icon_url=self.client.user.avatar_url)
                        em.description = f"{self.fail} Sorry but you didn't respond in time!"
                        em.set_footer(
                            text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                        await sent.edit(embed=em)
                elif msg.content.casefold() == "welchan":
                    await msg.delete()
                    em = Embed(color=color)
                    em.set_author(name="Cairo setup wizard",
                                  icon_url=self.client.user.avatar_url)
                    em.description = "Thanks for responding to the message, please respond by\nA). Mentioning a channel\nB). Giving me a channel ID"
                    em.add_field(name="Example of how to respond",
                                 value="```<#796866034534580264>``` or ```796866034534580264```")
                    em.set_footer(
                        text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                    await sent.edit(embed=em)
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
                            em.set_author(name="Cairo setup wizard",
                                          icon_url=self.client.user.avatar_url)
                            em.description = f"I set the ID to ``{y}``"
                            em.add_field(name=f"{self.check} Thank your for using Cairo setup wizard!",
                                         value=f"I have finished all my tasks!")
                            em.set_footer(
                                text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                            await sent.edit(embed=em)
                            result = await self.client.db.fetchrow("SELECT channel_id FROM db.welcome WHERE guild_id = $1", ctx.guild.id)
                            if result == None:
                                await self.client.db.execute("INSERT INTO db.welcome(guild_id, channel_id) VALUES($1, $2)", ctx.guild.id, int(y))
                            elif result != None:
                                await self.client.db.execute("UPDATE db.welcome SET channel_id = $1 WHERE guild_id = $2", int(y), ctx.guild.id)
                    except asyncio.TimeoutError:
                        em = Embed(color=color)
                        em.set_author(name="Cairo setup wizard",
                                      icon_url=self.client.user.avatar_url)
                        em.description = f"{self.fail} Sorry but you didn't respond in time!"
                        em.set_footer(
                            text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                        await sent.edit(embed=em)
                elif msg.content.casefold() == "goodchan":
                    await msg.delete()
                    em = Embed(color=color)
                    em.set_author(name="Cairo setup wizard",
                                  icon_url=self.client.user.avatar_url)
                    em.description = "Thanks for responding to the message, please respond by\nA). Mentioning a channel\nB). Giving me a channel ID"
                    em.add_field(name="Example of how to respond",
                                 value="```<#796866034534580264>``` or ```796866034534580264```")
                    em.set_footer(
                        text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                    await sent.edit(embed=em)
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
                            em.set_author(name="Cairo setup wizard",
                                          icon_url=self.client.user.avatar_url)
                            em.description = f"I set the ID to ``{y}``"
                            em.add_field(name=f"{self.check} Thank your for using Cairo setup wizard!",
                                         value=f"I have finished all my tasks!")
                            em.set_footer(
                                text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                            await sent.edit(embed=em)
                            result = await self.client.db.fetchrow("SELECT channel_id FROM db.goodbye WHERE guild_id = $1", ctx.guild.id)
                            if result == None:
                                await self.client.db.execute("INSERT INTO db.goodbye(guild_id, channel_id) VALUES($1, $2)", ctx.guild.id, int(y))
                            elif result != None:
                                await self.client.db.execute("UPDATE db.goodbye SET channel_id = $1 WHERE guild_id = $2", int(y), ctx.guild.id)
                    except asyncio.TimeoutError:
                        em = Embed(color=color)
                        em.set_author(name="Cairo setup wizard",
                                      icon_url=self.client.user.avatar_url)
                        em.description = f"{self.fail} Sorry but you didn't respond in time!"
                        em.set_footer(
                            text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                        await sent.edit(embed=em)
                elif msg.content.casefold() == "remlogs":
                    result = await self.client.db.execute("SELECT channel_id FROM db.modlog WHERE guild_id = $1", ctx.guild.id)
                    if result == None:
                        await msg.delete()
                        em = Embed(color=color)
                        em.set_author(name="Cairo setup wizard",
                                      icon_url=self.client.user.avatar_url)
                        em.add_field(name=f"{self.fail} Error encountered",
                                     value=f"Your log channel is not in the database")
                        em.set_footer(
                            text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                        await sent.edit(embed=em)
                    elif result != None:
                        await self.client.db.execute("DELETE FROM db.modlog WHERE guild_id = $1", ctx.guild.id)
                        await msg.delete()
                        em = Embed(color=color)
                        em.set_author(name="Cairo setup wizard",
                                      icon_url=self.client.user.avatar_url)
                        em.add_field(
                            name=f"{self.check} Success!", value="Removed your log channel from the database")
                        em.set_footer(
                            text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                        await sent.edit(embed=em)
                elif msg.content.casefold() == "remwel":
                    result = await self.client.db.fetchrow("SELECT msg FROM db.welcome WHERE guild_id = $1", ctx.guild.id)
                    try:
                        if result is None:
                            await msg.delete()
                            em = Embed(color=color)
                            em.set_author(name="Cairo setup wizard",
                                      icon_url=self.client.user.avatar_url)
                            em.add_field(name=f"{self.fail} Error encountered",
                                     value=f"Your welcome items are not in the database")
                            em.set_footer(
                                text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                            await sent.edit(embed=em)
                        elif result is not None:
                            await self.client.db.execute("DELETE FROM db.welcome WHERE guild_id = $1", ctx.guild.id)
                            await msg.delete()
                            em = Embed(color=color)
                            em.set_author(name="Cairo setup wizard",
                                      icon_url=self.client.user.avatar_url)
                            em.add_field(
                                name=f"{self.check} Success!", value="Removed your welcome items from the database")
                            em.set_footer(
                                text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                            await sent.edit(embed=em)
                    except Exception as e:
                        print(e)
                elif msg.content.casefold() == "remgood":
                    result = await self.client.db.fetchrow("SELECT msg FROM db.goodbye WHERE guild_id = $1", ctx.guild.id)
                    try:
                        if result is None:
                            await msg.delete()
                            em = Embed(color=color)
                            em.set_author(name="Cairo setup wizard",
                                      icon_url=self.client.user.avatar_url)
                            em.add_field(name=f"{self.fail} Error encountered",
                                     value=f"Your goodbye items are not in the database")
                            em.set_footer(
                                text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                            await sent.edit(embed=em)
                        elif result is not None:
                            await self.client.db.execute("DELETE FROM db.goodbye WHERE guild_id = $1", ctx.guild.id)
                            await msg.delete()
                            em = Embed(color=color)
                            em.set_author(name="Cairo setup wizard",
                                      icon_url=self.client.user.avatar_url)
                            em.add_field(
                                name=f"{self.check} Success!", value="Removed your goodbye items from the database")
                            em.set_footer(
                                text=f"Cairo setup wizard | Requested by {ctx.author.name}", icon_url=self.client.user.avatar_url)
                            await sent.edit(embed=em)
                    except Exception as e:
                        print(e)

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
                res = await self.client.db.fetchrow("SELECT prefix FROM db.prefixes WHERE guild_id = $1", ctx.guild.id)
                if res != None:
                    await self.client.db.execute("UPDATE db.prefixes SET prefix = $1 WHERE guild_id = $2", prefix, ctx.guild.id)
                elif res == None:
                    await self.client.db.execute("INSERT INTO db.prefixes(guild_id, prefix) VALUES($1, $2)", ctx.guild.id, "$")
                    await self.client.db.execute("UPDATE db.prefixes SET prefix = $1 WHERE guild_id = $2", prefix, ctx.guild.id)
                em = Embed(color=color)
                em.description = f"{self.check} Set the prefix to {prefix}"
                await ctx.send(embed=em)
            except Exception as e:
                await ctx.send("{}" .format(e))


def setup(client):
    client.add_cog(SetupClass(client))
