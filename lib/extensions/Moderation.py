import discord
import aiosqlite
import asyncpg
import os
import time
import asyncio
from dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands


color = 0xfffafa  # 0xff4500  # 0x4B0082


OWNER_IDS = [541722893747224589]

load_dotenv()
IP = os.getenv("IP")
load_dotenv()
PASSWD = os.getenv("PASSWD")
load_dotenv()
DB = os.getenv("DB")


class administrator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason="No reason provided"):
        t = time.localtime()
        current_time = time.strftime("%I:%M %p", t)
        if member == None:
            em = discord.Embed(color=color)
            em.title = "Ban command"
            em.description = """
            INFO: [] = required, {} = optional
            Requires = Ban member
            Arguments = [member] {reason}
            Description = Bans a member
            """
            em.set_footer(icon_url=ctx.author.avatar_url,
                          text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=em)
        elif member != None:
            try:
                result = await self.client.db.fetchrow(f"SELECT channel_id FROM aquhx.modlog WHERE guild_id = $1", ctx.guild.id)
                if result == None:
                    c = await member.create_dm()
                    await c.send(f"You have been banned from **{ctx.guild.name}**, **Reason:** {reason}" .format(reason))
                    await member.ban(reason=reason)
                    await ctx.message.delete()
                    embed = discord.Embed(color=discord.Color.green())
                    embed.description = f"✅ Banned **{member.name}** for **{reason}" .format(
                        reason)
                elif result != None:
                    channel = self.client.get_channel(int(result[0]))
                    em = discord.Embed(color=0xff0000)
                    em.title = "Member banned"
                    em.set_footer(
                        text=f'Member ID: {member.id}', icon_url=member.avatar_url)
                    em.description = f"""
                    Member banned: **{member.mention}**
                    Command operator: **{ctx.author.mention}**
                    Reason for being banned: **{reason}**
                    Time of ban: **{current_time}**
                    """ .format(reason)
                    em.set_thumbnail(url=ctx.author.avatar_url)
                    await channel.send(embed=em)
                    c = await member.create_dm()
                    await c.send(f"You have been banned from **{ctx.guild.name}**, **Reason:** {reason}" .format(reason))
                    await member.ban(reason=reason)
                    await ctx.message.delete()
                    embed = discord.Embed(color=discord.Color.green())
                    embed.description = f"✅ Banned **{member.name}** for **{reason}**".format(
                        reason)
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send("{}" .format(e))

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason="No reason provided"):
        t = time.localtime()
        current_time = time.strftime("%I:%M %p", t)
        if member == None:
            em = discord.Embed(color=color)
            em.title = "Kick command"
            em.description = """
            INFO: [] = required, {} = optional
            Requires = Kick member
            Arguments = [member] {reason}
            Description = Kicks a member
            """
            em.set_footer(icon_url=ctx.author.avatar_url,
                          text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=em)
        elif member != None:
            try:
                result = await self.client.db.fetchrow(f"SELECT channel_id FROM aquhx.modlog WHERE guild_id = $1", ctx.guild.id)
                if result == None:
                    c = await member.create_dm()
                    await c.send(f"You have been kicked from **{ctx.guild.name}**, **Reason:** {reason}" .format(reason))
                    await member.kick(reason=reason)
                    await ctx.message.delete()
                    embed = discord.Embed(color=discord.Color.green())
                    embed.description = f"✅ Kicked **{member.name}** for **{reason}" .format(
                        reason)
                elif result != None:
                    channel = self.client.get_channel(int(result[0]))
                    em = discord.Embed(color=0xff0000)
                    em.title = "Member kicked"
                    em.set_footer(
                        text=f'Member ID: {member.id}', icon_url=member.avatar_url)
                    em.description = f"""
                    Member kicked: **{member.mention}**
                    Command operator: **{ctx.author.mention}**
                    Reason for being banned: **{reason}**
                    Time of ban: **{current_time}**
                    """ .format(reason)
                    em.set_thumbnail(url=ctx.author.avatar_url)
                    await channel.send(embed=em)
                    c = await member.create_dm()
                    await c.send(f"You have been kicked from **{ctx.guild.name}**, **Reason:** {reason}" .format(reason))
                    await member.kick(reason=reason)
                    await ctx.message.delete()
                    embed = discord.Embed(color=discord.Color.green())
                    embed.description = f"✅ Kicked **{member.name}** for **{reason}**".format(
                        reason)
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send("{}" .format(e))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userID=None):
        t = time.localtime()
        current_time = time.strftime("%I:%M %p", t)
        if userID == None:
            em = discord.Embed(color=color)
            em.title = "Unban command"
            em.description = """
            INFO: [] = required, {} = optional
            Requires = Ban member
            Arguments = [user]
            Description = Unbans a user
            """
            em.set_footer(icon_url=ctx.author.avatar_url,
                          text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=em)
        elif userID != None:
            try:
                result = await self.client.db.fetchrow(f"SELECT channel_id FROM aquhx.modlog WHERE guild_id = $1", ctx.guild.id)
                if result == None:
                    username = await self.client.fetch_user(int(userID))
                    user = discord.Object(id=userID)
                    await ctx.guild.unban(user)
                    await ctx.message.delete()
                    embed = discord.Embed(color=discord.Color.green())
                    embed.description = f"✅ Unbanned **{username}**"
                elif result != None:
                    channel = self.client.get_channel(int(result[0]))
                    username = await self.client.fetch_user(int(userID))
                    user = discord.Object(id=userID)
                    await ctx.guild.unban(user)
                    await ctx.message.delete()
                    embed = discord.Embed(color=discord.Color.green())
                    embed.description = f"✅ Unbanned **{username}**"
                    em = discord.Embed(color=discord.Color.green())
                    em.title = "User unbanned"
                    em.set_footer(
                        text=f'user ID: {userID}')
                    em.description = f"""
                    User unbanned: **{username}**
                    Command operator: **{ctx.author.mention}**
                    Time of unban: **{current_time}**
                    """
                    em.set_thumbnail(url=ctx.author.avatar_url)
                    await channel.send(embed=em)
                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send("{}" .format(e))

    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        t = time.localtime()
        current_time = time.strftime("%I:%M %p", t)
        if amount == None:
            em = discord.Embed(color=color)
            em.title = "Clear command"
            em.description = """
            INFO: [] = required, {} = optional
            Requires = Manage messages
            Arguments = [amount]
            Description = Clears messages
            """
            em.set_footer(icon_url=ctx.author.avatar_url,
                          text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=em)
        elif amount != None:
            try:
                result = await self.client.db.fetchrow(f"SELECT channel_id FROM aquhx.modlog WHERE guild_id = $1", ctx.guild.id)
                if result == None:
                    await ctx.channel.purge(limit=amount + 1)
                    em = discord.Embed(color=discord.Color.green())
                    em.description = f"✅ Purged **{amount+1}** message(s)"
                    await asyncio.sleep(3)
                elif result != None:
                    channel = self.client.get_channel(int(result[0]))
                    await ctx.channel.purge(limit=amount + 1)
                    em = discord.Embed(color=discord.Color.green())
                    em.description = f"✅ Purged **{amount+1}** message(s)"
                    await asyncio.sleep(3)
                    embed = discord.Embed(color=discord.Color.green())
                    embed.title = "Messages purged"
                    embed.set_footer(
                        text=f'{amount + 1} message(s) cleared', icon_url=ctx.author.avatar_url)
                    embed.description = f"""
                    Messages cleared: **{amount + 1}**
                    Command operator: **{ctx.author.mention}**
                    Time of purge: **{current_time}**
                    """
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    await channel.send(embed=embed)
                sent = await ctx.send(embed=em)
                await asyncio.sleep(3)
                await sent.delete()

            except Exception as e:
                await ctx.send("{}" .format(e))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member = None):
        t = time.localtime()
        current_time = time.strftime("%I:%M %p", t)
        if member == None:
            em = discord.Embed(color=color)
            em.title = "Mute command"
            em.description = """
            INFO: [] = required, {} = optional
            Requires = Manage messages
            Arguments = [member]
            Description = Mutes member
            """
            em.set_footer(icon_url=ctx.author.avatar_url,
                          text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=em)
        elif member != None:
            try:
                result = await self.client.db.fetchrow(f"SELECT channel_id FROM aquhx.modlog WHERE guild_id = $1", ctx.guild.id)
                role = get(ctx.guild.roles, name="Muted")
                if result == None:
                    await ctx.message.delete()
                    await member.add_roles(role)
                    em = discord.Embed(color=discord.Color.green())
                    em.description = f"✅ Muted {member.mention}"
                elif result != None:
                    channel = self.client.get_channel(int(result[0]))
                    await ctx.message.delete()
                    await member.add_roles(role)
                    em = discord.Embed(color=discord.Color.green())
                    em.description = f"✅ Muted {member.mention}"
                    embed = discord.Embed(color=0xff0000)
                    embed.title = "Member muted"
                    embed.set_footer(
                        text=f'Member ID: {member.id}', icon_url=member.avatar_url)
                    embed.description = f"""
                    Member muted: **{member.mention}**
                    Command operator: **{ctx.author.mention}**
                    Time of mute: **{current_time}**
                    """
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    await channel.send(embed=embed)
                await ctx.send(embed=em)
            except Exception as e:
                await ctx.send("{}" .format(e))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member = None):
        t = time.localtime()
        current_time = time.strftime("%I:%M %p", t)
        if member == None:
            em = discord.Embed(color=color)
            em.title = "Unmute command"
            em.description = """
            INFO: [] = required, {} = optional
            Requires = Manage messages
            Arguments = [member]
            Description = Unmutes member
            """
            em.set_footer(icon_url=ctx.author.avatar_url,
                          text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=em)
        elif member != None:
            try:
                result = await self.client.db.fetchrow(f"SELECT channel_id FROM aquhx.modlog WHERE guild_id = $1", ctx.guild.id)
                role = get(ctx.guild.roles, name="Muted")
                if result == None:
                    await ctx.message.delete()
                    await member.remove_roles(role)
                    em = discord.Embed(color=discord.Color.green())
                    em.description = f"✅ Unmuted {member.mention}"
                elif result != None:
                    channel = self.client.get_channel(int(result[0]))
                    await ctx.message.delete()
                    await member.remove_roles(role)
                    em = discord.Embed(color=discord.Color.green())
                    em.description = f"✅ Unmuted {member.mention}"
                    embed = discord.Embed(color=discord.Color.green())
                    embed.title = "Member unmuted"
                    embed.set_footer(
                        text=f'Member ID: {member.id}', icon_url=member.avatar_url)
                    embed.description = f"""
                    Member unmuted: **{member.mention}**
                    Command operator: **{ctx.author.mention}**
                    Time of unmute: **{current_time}**
                    """
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    await channel.send(embed=embed)
                await ctx.send(embed=em)
            except Exception as e:
                await ctx.send("{}" .format(e))


def setup(client):
    client.add_cog(administrator(client))
