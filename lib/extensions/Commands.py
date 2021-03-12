import discord
import time
import asyncpg
import os
from dotenv import load_dotenv
import asyncio
from typing import List, Union
from discord.ext import commands


color = 0xfffafa  # 0xff4500  # 0x4B0082


load_dotenv()
IP = os.getenv("IP")
load_dotenv()
PASSWD = os.getenv("PASSWD")
load_dotenv()
DB = os.getenv("DB")


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def say(self, ctx, *, words=None):
        t = time.localtime()
        current_time = time.strftime("%I:%M %p", t)
        if words == None:
            em = discord.Embed(color=color)
            em.title = "Say command"
            em.description = """
            Requires = Nothing
            Arguments = [words]
            Description = Say something
            """
            em.set_footer(icon_url=ctx.author.avatar_url,
                          text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=em)
        elif words != None:
            try:
                result = await self.client.db.fetchrow(f"SELECT channel_id FROM aquhx.modlog WHERE guild_id = $1", ctx.guild.id)
                if result == None:
                    await ctx.message.delete()
                    await asyncio.sleep(.5)
                    if "@everyone" in words:
                        return
                elif result != None:
                    if "@everyone" in words:
                        return
                    channel = self.client.get_channel(int(result[0]))
                    await ctx.message.delete()
                    await asyncio.sleep(.5)
                    embed = discord.Embed(color=discord.Color.green())
                    embed.title = "Said something"
                    embed.set_footer(
                        text=f'Ran by {ctx.author.name}', icon_url=ctx.author.avatar_url)
                    embed.description = f"""
                    Command operator: **{ctx.author.mention}**
                    Time of unmute: **{current_time}**
                    """
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    await channel.send(embed=embed)
                await ctx.send("{}".format(words))
            finally:
                return

    @commands.command()
    async def embed(self, ctx, *, words=None):
        if words == None:
            em = discord.Embed(color=color)
            em.title = "Embed command"
            em.description = """
            Requires = Nothing
            Arguments = [words]
            Description = Embed something
            """
            em.set_footer(icon_url=ctx.author.avatar_url,
                          text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=em)
        elif words != None:
            if "@here" in words:
                if ctx.author.advanced:
                    await ctx.message.delete()
                    await asyncio.sleep(.5)
                    em = discord.Embed(color=color)
                    em.set_author(icon_url=ctx.author.avatar_url,
                                  name=ctx.author.name)
                    em.description = "{}" .format(words)
                    await ctx.send(embed=em)
                else:
                    return
            elif "@everyone" in words:
                if ctx.author.advanced:
                    await ctx.message.delete()
                    await asyncio.sleep(.5)
                    em = discord.Embed(color=color)
                    em.set_author(icon_url=ctx.author.avatar_url,
                                  name=ctx.author.name)
                    em.description = "{}" .format(words)
                    await ctx.send(embed=em)
                else:
                    return
            await ctx.message.delete()
            await asyncio.sleep(.5)
            em = discord.Embed(color=color)
            em.set_author(icon_url=ctx.author.avatar_url,
                          name=ctx.author.name)
            em.description = "{}" .format(words)
            await ctx.send(embed=em)

    @commands.command(aliases=['vote'])
    async def poll(self, ctx, *, words):
        if words == None:
            em = discord.Embed(color=color)
            em.title = "Poll command"
            em.description = """
            Requires = Nothing
            Arguments = [words]
            Description = Vote on something
            """
            em.set_footer(icon_url=ctx.author.avatar_url,
                          text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=em)
        elif words != None:
            em = discord.Embed(color=color)
            em.title = "🗳 Vote now!"
            em.description = "{}" .format(words)
            message = await ctx.send(embed=em)
            await message.add_reaction('✅')
            await message.add_reaction('❌')

    @commands.command()
    async def help(self, ctx):
        t = time.localtime()
        current_time = time.strftime("%I:%M %p", t)
        emb = discord.Embed(color=color)
        emb.set_author(icon_url=self.client.user.avatar_url,
                       name="Aquhx help list")
        emb.add_field(name="⚒️ Moderation commands",
                      value="For mods+ only, these commands are very dangerous")
        emb.add_field(name="⚙️ Configuration commands",
                      value="For mods+ only, these commands configure the bot for your server")
        emb.add_field(name="🌐 Regular commands",
                      value="These commands are for regular folks, anyone can use these")
        emb.set_footer(
            text=f"Requested by {ctx.author.name} at {current_time}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=emb)
        await msg.add_reaction('⚒️')
        await msg.add_reaction('⚙️')
        await msg.add_reaction('🌐')
        await msg.add_reaction('🏠')
        em1 = discord.Embed(color=color)
        em1.set_author(icon_url=self.client.user.avatar_url,
                       name="Aquhx moderation list")
        em1.add_field(name="Ban", value="Ban a member")
        em1.add_field(name="Unban", value="Unban a user")
        em1.add_field(name="Kick", value="Kick a member")
        em1.add_field(name="Mute", value="Mute a member")
        em1.add_field(name="Unmute", value="Unmute a member")
        em1.add_field(name="Clear", value="Purge some messages")
        em1.set_footer(
            text=f"Requested by {ctx.author.name} at {current_time}", icon_url=ctx.author.avatar_url)
        em2 = discord.Embed(color=color)
        em2.set_author(icon_url=self.client.user.avatar_url,
                       name="Aquhx configuration list")
        em2.add_field(name="configlogs",
                      value="Configure your logging channel")
        em2.add_field(name="deletelogs",
                      value="Delete your channel from the database")
        em2.set_footer(
            text=f"Requested by {ctx.author.name} at {current_time}", icon_url=ctx.author.avatar_url)

        em3 = discord.Embed(color=color)
        em3.set_author(icon_url=self.client.user.avatar_url,
                       name="Aquhx command list")
        em3.add_field(name="Say", value="Say something")
        em3.add_field(name="Embed", value="Embed something")
        em3.add_field(name="Poll", value="Vote on something")
        em3.set_footer(
            text=f"Requested by {ctx.author.name} at {current_time}", icon_url=ctx.author.avatar_url)

        def reac_check(r, u):
            return u == ctx.author and msg.id == r.message.id and u != self.client.user and r.emoji in ['⚒️', '⚙️', '🌐', '🏠']

        loop = True
        while loop == True:
            try:
                reaction, user = await self.client.wait_for('reaction_add', check=reac_check)
                em = str(reaction.emoji)

            except TimeoutError:
                pass
                break  # we exit the loop

            if user != self.client.user:
                await msg.remove_reaction(emoji=em, member=user)

            if em == '⚒️':
                await msg.edit(embed=em1)
                await msg.add_reaction('🏠')

            if em == '⚙️':
                await msg.edit(embed=em2)
                await msg.add_reaction('🏠')

            if em == '🌐':
                await msg.edit(embed=em3)
                await msg.add_reaction('🏠')

            if em == '🏠':
                await msg.edit(embed=emb)
                await msg.add_reaction('🏠')


def setup(client):
    client.add_cog(Fun(client))
