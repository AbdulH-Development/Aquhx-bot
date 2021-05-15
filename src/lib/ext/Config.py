"""
copyright (c) 2021-present DevCairo
license GPL v3, see LICENSE for more details.
"""

from discord.ext.commands import *
from discord.ext import *
from colorama import Fore
from discord import *
import asyncio
 
from typing_extensions import ParamSpec


class Config(Cog):
    def __init__(self, client):
        self.client = client

    @command()
    @has_permissions(manage_guild=True)
    async def setup(self, ctx):
        em = Embed(color=self.client.color)
        em.set_author(name="Cairo setup", icon_url=self.client.user.avatar_url)
        em.description = "Please respond with the icon of the setup category!"
        em.add_field(name="📰 Logs", value="Setup logging")
        em.add_field(name="👋 Welconf", value="Setup your welcome objects")
        em.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        sent = await ctx.send(embed=em)
        await sent.add_reaction('📰')
        await sent.add_reaction('👋')

        def reac_check(r, u):
            return u == ctx.author and sent.id == r.message.id and u != self.client.user and r.emoji in ['📰', '👋']

        loop = True
        while loop == True:
            try:
                reaction, user = await self.client.wait_for('reaction_add', check=reac_check)
                em = str(reaction.emoji)

            except asyncio.TimeoutError:
                em = Embed(color=self.client.color)
                em.set_author(name="Cairo setup",
                              icon_url=self.client.user.avatar_url)
                em.description = "You didn't respond!"
                em.add_field(name="📰 Logs", value="Setup logging")
                em.set_footer(
                    text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                await sent.edit(embed=em)

            if user != self.client.user:
                await sent.remove_reaction(emoji=em, member=user)

            if user != ctx.author:
                await sent.remove_reaction(emoji=em, member=user)
                

            if em == "📰":
                try:
                    await sent.delete()
                    await ctx.invoke(self.client.get_command("logs"))
                except Exception as e:
                    print("[ " + Fore.RED + "ERR" + Fore.RESET + f" ] {e}")
            elif em == "👋":
                try:
                    await sent.delete()
                    await ctx.invoke(self.client.get_command("welconf"))
                except Exception as e:
                    print("[ " + Fore.RED + "ERR" + Fore.RESET + f" ] {e}")

    @command(aliases=["log"])
    @has_permissions(manage_guild=True)
    async def logs(self, ctx):
        em = Embed(color=self.client.color)
        em.set_author(name="Cairo setup",
                      icon_url=self.client.user.avatar_url)
        em.description = "Thanks for using Cairo setup!\nPlease respond to this message by mentioning a channel\nor giving me a channel ID"
        em.set_footer(text=f"Requested by {ctx.author.name}")
        sent = await ctx.send(embed=em)
        try:
            msg = await self.client.wait_for(
                'message',
                timeout=60.0,
                check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
            if msg:
                try:
                    original = msg.content
                    await msg.delete()

                    x = original.replace("<#", "")
                    y = x.replace(">", "")
                    chanID = int(y)
                    await self.client.cursor.execute("SELECT channel_id FROM modlog WHERE guild_id = %s", (ctx.guild.id,))
                    fetch = await self.client.cursor.fetchone()
                    if fetch == None:
                        await self.client.cursor.execute("INSERT INTO modlog (guild_id, channel_id) VALUES (%s, %s)", (ctx.guild.id, chanID))
                    elif fetch != None:
                        await self.client.cursor.execute("UPDATE modlog SET channel_id = %s WHERE guild_id = %s", (chanID, ctx.guild.id))
                    embed = Embed(color=self.client.color)
                    embed.set_author(name="Cairo setup",
                                     icon_url=self.client.user.avatar_url)
                    embed.description = f"{self.client.check} Thanks for using Cairo setup!\nI set your logging channel to <#{chanID}>"
                    embed.set_footer(
                        text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                    await sent.edit(embed=embed)
                except Exception as e:
                    print("[ " + Fore.RED + "ERR" + Fore.RESET + f" ] {e}")
        except asyncio.TimeoutError:
            em = Embed(color=self.client.color)
            em.title = f"{self.client.fail} You didn't respond in time!"
            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
            await sent.edit()



    @command()
    @has_permissions(manage_guild=True)
    async def welconf(self, ctx):
        em = Embed(color=self.client.color)
        em.set_author(name="Cairo setup", icon_url=self.client.user.avatar_url)
        em.title = "Configure a welcome object"
        em.add_field(name="👋 message", value="The message that will be sent")
        em.add_field(name="⛓️ channel", value="The channel where the message will be sent")
        em.add_field(name="🔗 embed", value="Same as message but with more options")
        em.add_field(name="🗑️ remove", value="Remove all welcome objects from the database")
        em.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        sent = await ctx.send(embed=em)
        await sent.add_reaction("👋")
        await sent.add_reaction("⛓️")
        await sent.add_reaction("🔗")
        await sent.add_reaction("🗑️")


        def reac_check(r, u):
            return u == ctx.author and sent.id == r.message.id and u != self.client.user and r.emoji in ['👋', '⛓️', '🔗', '🗑️']
    
        loop = True
        while loop == True:
            try:
                reaction, user = await self.client.wait_for('reaction_add', check=reac_check)
                em = str(reaction.emoji)
            except asyncio.TimeoutError:
                em = Embed(color=self.client.color)
                em.set_author(name="Cairo setup", icon_url=self.client.user.avatar_url)
                em.title = "You ran out of time to react!"
                em.add_field(name="👋 message", value="The message that will be sent")
                em.add_field(name="⛓️ channel",
                     value="The channel where the message will be sent")
                em.add_field(name="🔗 embed",
                     value="Same as message but with more options")
                em.set_footer(
                    text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                await sent.edit(embed=em)
                await sent.add_reaction("👋")
                await sent.add_reaction("⛓️")
                await sent.add_reaction("🔗")


            if user != self.client.user:
                await sent.remove_reaction(emoji=em, member=user)

            if user != ctx.author:
                await sent.remove_reaction(emoji=em, member=user)

            if em == "👋":
                await sent.clear_reactions()
                em = Embed(color=self.client.color)
                em.set_author(name="Cairo setup",
                              icon_url=self.client.user.avatar_url)
                em.title = "Please give me a message to add to my database"
                em.description = "```Arguments:\n{member} = username\n{mention} = user mention\n{guild} = guild name\n{members} = amount of members```"
                em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                await sent.edit(embed=em)
                try:
                    msg = await self.client.wait_for(
                        'message',
                        timeout=60.0,
                        check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                    if msg:
                        try:
                            await msg.delete()
                            await self.client.cursor.execute("SELECT welcome FROM welcome WHERE guild_id = %s", (ctx.guild.id, ))
                            fetch = await self.client.cursor.fetchone()
                            if fetch == None:
                                await self.client.cursor.execute("INSERT INTO welcome (guild_id, welcome) VALUES(%s, %s)", (ctx.guild.id, msg.content))
                            elif fetch != None:
                                await self.client.cursor.execute("UPDATE welcome SET welcome = %s WHERE guild_id = %s", (msg.content, ctx.guild.id, ))
                            em = Embed(color=self.client.color)
                            em.set_author(name="Cairo setup", icon_url=self.client.user.avatar_url)
                            em.description = f"{self.client.check} I set your welcome message to\n{msg.content}"
                            em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                            await sent.edit(embed=em)
                        except Exception as e:
                            print("[ " + Fore.RED + "ERR" + Fore.RESET + f" ] {e}")
                except asyncio.TimeoutError:
                    em = Embed(color=self.client.color)
                    em.set_author(name="Cairo setup",
                              icon_url=self.client.user.avatar_url)
                    em.set_author(name="Cairo setup", icon_url=self.client.user.avatar_url)
                    em.description = "You didn't respond in time!"
                    em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                    await sent.edit(embed=em)
            elif em == "⛓️":
                await sent.clear_reactions()
                em = Embed(color=self.client.color)
                em.set_author(name="Cairo setup",
                              icon_url=self.client.user.avatar_url)
                em.description = "Thanks for using Cairo setup!\nPlease respond to this message by mentioning a channel\nor giving me a channel ID or to\nmake me send the message to the user just say member"
                em.set_footer(
                    text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                await sent.edit(embed=em)
                try:
                    msg = await self.client.wait_for(
                        'message',
                        timeout=60.0,
                        check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                    if msg:
                        try:
                            original = msg.content
                            await msg.delete()

                            if original.casefold() == "member":
                                await self.client.cursor.execute("SELECT welchan FROM welcome WHERE guild_id = %s", (ctx.guild.id,))
                                fetch = await self.client.cursor.fetchone()
                                if fetch == None:
                                    await self.client.cursor.execute("INSERT INTO welcome (guild_id, welchan) VALUES(%s, %s)", (ctx.guild.id, "member", ))
                                elif fetch != None:\
                                    await self.client.cursor.execute("UPDATE welcome SET welchan = %s WHERE guild_id = %s", ("member", ctx.guild.id, ))
                                chanID = "member"
                            else:
                                x = original.replace("<#", "")
                                y = x.replace(">", "")
                                chanID = int(y)
                                await self.client.cursor.execute("SELECT welchan FROM welcome WHERE guild_id = %s", (ctx.guild.id,))
                                fetch = await self.client.cursor.fetchone()
                                if fetch == None:
                                    await self.client.cursor.execute("INSERT INTO welcome (guild_id, welchan) VALUES (%s, %s)", (ctx.guild.id, chanID))
                                elif fetch != None:
                                    await self.client.cursor.execute("UPDATE welcome SET welchan = %s WHERE guild_id = %s", (chanID, ctx.guild.id))
                            embed = Embed(color=self.client.color)
                            embed.set_author(name="Cairo setup",
                                     icon_url=self.client.user.avatar_url)
                            embed.description = f"{self.client.check} Thanks for using Cairo setup!\nI set your welcome channel to <#{chanID}>"
                            embed.set_footer(
                                text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                            await sent.edit(embed=embed)
                        except Exception as e:
                            print("[ " + Fore.RED + "ERR" + Fore.RESET + f" ] {e}")
                except asyncio.TimeoutError:
                    em = Embed(color=self.client.color)
                    em.title = f"{self.client.fail} You didn't respond in time!"
                    em.set_footer(
                        text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                    await sent.edit()
            elif em == "🗑️":
                await sent.clear_reactions()
                await self.client.cursor.execute("SELECT welcome, welchan FROM welcome WHERE guild_id = %s", (ctx.guild.id, ))
                fetch = await self.client.cursor.fetchone()
                if fetch == None:
                    em = Embed(color=self.client.color)
                    em.set_author(name="Cairo setup",
                              icon_url=self.client.user.avatar_url)
                    em.description = f"{self.client.fail} Sorry but I could not find any welcome objects for this server!"
                    em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                    await sent.edit(embed=em)
                elif fetch != None:
                    await self.client.cursor.execute("DELETE FROM welcome WHERE guild_id = %s", (ctx.guild.id, ))
                    em = Embed(color=self.client.color)
                    em.set_author(name="Cairo setup",
                                  icon_url=self.client.user.avatar_url)
                    em.description = f"{self.client.check} I have removed all your welcome objects from the database!"
                    em.set_footer(
                        text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                    await sent.edit(embed=em)
            elif em == "🔗":
                em = Embed(color=self.client.color)
                em.set_author(name="Cairo setup", icon_url=self.client.user.avatar_url)
                em.description = "Thanks for using Cairo!\nPlease respond to this message\nwith a title for your embed."
                em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                await sent.edit(embed=em)
                try:
                    msg = await self.client.wait_for(
                        'message',
                        timeout=60.0,
                        check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                    if msg:
                        try:
                            await self.client.cursor.execute("SELECT title FROM welembed WHERE guild_id = %s", (ctx.guild.id, ))
                            fetch = await self.client.cursor.fetchone()
                            if fetch == None:
                                await self.client.cursor.execute("INSERT INTO welembed(guild_id, title) VALUES(%s, %s)", (ctx.guild.id, msg.content, ))
                            elif fetch != None:
                                await self.client.cursor.execute("UPDATE welembed SET title = %s WHERE guild_id = %s", (msg.content, ctx.guild.id, ))
                            em = Embed(color=self.client.color)
                            em.set_author(name="Cairo setup",
                              icon_url=self.client.user.avatar_url)
                            em.description = f"I set your embed title to **{msg.content}**\nPlease provide me with a message for the member!"
                            em.set_footer(
                                text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                            await sent.edit(embed=em)
                            try:
                                msg = await self.client.wait_for(
                                    'message',
                                    timeout=60.0,
                                    check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                                if msg:
                                    try:
                                        await self.client.cursor.execute("SELECT message FROM welembed WHERE guild_id = %s", (ctx.guild.id, ))
                                        fetch = await self.client.cursor.fetchone()
                                        if fetch == None:
                                            await self.client.cursor.execute("INSERT INTO welembed (guild_id, message) VALUES(%s, %s)", (ctx.guild.id, msg.content))
                                        elif fetch != None:
                                            await self.client.cursor.execute("UPDATE welembed SET message = %s WHERE guild_id = %s", (msg.content, ctx.guild.id, ))
                                        em = Embed(color=self.client.color)
                                        em.set_author(name="Cairo setup", icon_url=self.client.user.avatar_url)
                                        em.description = f"I set the message to {msg.content}!\nNext I need an image, please respond with a link or say skip to not add one"
                                        em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                                        await sent.edit(embed=em)
                                        try:
                                            msg = await self.client.wait_for(
                                            'message',
                                            timeout=60.0,
                                            check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                                            if msg:
                                                try:
                                                    if msg.content.casefold() == "skip":
                                                        pass
                                                    else:
                                                        await self.client.cursor.execute("SELECT im_url FROM welembed WHERE guild_id = %s", (ctx.guild.id, ))
                                                        fetch = await self.client.cursor.fetchone()
                                                        if fetch == None:
                                                            await self.client.cursor.execute("INSERT INTO welembed(guild_id, im_url) VALUES(%s, %s)", (ctx.guild.id, msg.content))
                                                        elif fetch != None:
                                                            await self.client.cursor.execute("UPDATE welembed SET im_url = %s WHERE guild_id = %s", (msg.content, ctx.guild.id))
                                                    em = Embed(color=self.client.color)
                                                    em.set_author(name="Cairo setup", icon_url=self.client.user.avatar_url)
                                                    em.description = f"I set the image!\nNext I need a thumbnail, please respond with a link or say skip to not add one"
                                                    em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                                                    await sent.edit(embed=em)
                                                    try:
                                                        msg = await self.client.wait_for(
                                                            'message',
                                                            timeout=60.0,
                                                            check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
                                                        if msg:
                                                            try:
                                                                if msg.content.casefold() == "skip":
                                                                    pass
                                                                else:
                                                                    await self.client.cursor.execute("SELECT th_url FROM welembed WHERE guild_id = %s", (ctx.guild.id, ))
                                                                    fetch = await self.client.cursor.fetchone()
                                                                    if fetch == None:
                                                                        await self.client.cursor.execute("INSERT INTO welembed(guild_id, th_url) VALUES(%s, %s)", (ctx.guild.id, msg.content, ))
                                                                    elif fetch != None:
                                                                        await self.client.cursor.execute("UPDATE welembed SET th_url = %s WHERE guild_id = %s", (msg.content, ctx.guild.id, ))
                                                                em = Embed(color=self.client.color)
                                                                em.set_author(name="Cairo setup", icon_url=self.client.user.avatar_url)
                                                                em.description = f"{self.client.check} Completed all tasks!\nThanks for using Cairo."
                                                                em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                                                                await sent.edit(embed=em)
                                                            except Exception as e:
                                                                print(
                                                                    "[ " + Fore.RED + "ERR" + Fore.RESET + f" ] {e}")
                                                    except asyncio.TimeoutError:
                                                        em = Embed(color=self.client.color)
                                                        em.title = f"{self.client.fail} You didn't respond in time!"
                                                        em.set_footer(
                                                           text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                                                        await sent.edit()
                                                except Exception as e:
                                                    print("[ " + Fore.RED + "ERR" + Fore.RESET + f" ] {e}")
                                        except asyncio.TimeoutError:
                                            em = Embed(color=self.client.color)
                                            em.title = f"{self.client.fail} You didn't respond in time!"
                                            em.set_footer(
                                                text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                                            await sent.edit()
                                    except Exception as e:
                                        print("[ " + Fore.RED + "ERR" + Fore.RESET + f" ] {e}")
                            except asyncio.TimeoutError:
                                em = Embed(color=self.client.color)
                                em.title = f"{self.client.fail} You didn't respond in time!"
                                em.set_footer(
                                   text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                                await sent.edit()
                        except Exception as e:
                            print("[ " + Fore.RED + "ERR" + Fore.RESET + f" ] {e}")
                except asyncio.TimeoutError:
                    em = Embed(color=self.client.color)
                    em.title = f"{self.client.fail} You didn't respond in time!"
                    em.set_footer(
                        text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                    await sent.edit()

def setup(client):
    client.add_cog(Config(client))
