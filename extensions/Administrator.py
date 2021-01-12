# First imports

import discord
import aiosqlite
import asyncio

# Secondary imports

from discord.ext import commands


color = 0x2e9bbb
errorc = 0xff0000
donec = 0x00c21d


class Administrator(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=None):
        db = await aiosqlite.connect("sql/main.sqlite")
        cursor = await db.execute(f"SELECT channel_id FROM logs WHERE guild_id = {ctx.guild.id}")
        result = await cursor.fetchone()
        if amount == None:
            em = discord.Embed(color=color)
            em.title = "Clear command"
            em.description = ";Clear {amount}"
            return await ctx.send(embed=em)
        elif result == None:
            await ctx.message.delete()
            await ctx.channel.purge(limit=int(amount))
            await ctx.send(f"Purged {amount} message(s)")
            await asyncio.sleep(3)
            await ctx.channel.purge(limit=1)
        elif result is not None:
            await ctx.message.delete()
            await ctx.channel.purge(limit=int(amount))
            await ctx.send(f"Purged {amount} message(s)")
            await asyncio.sleep(3)
            await ctx.channel.purge(limit=1)
            channel = self.client.get_channel(int(result[0]))
            log = discord.Embed(color=color)
            log.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            log.add_field(name="Moderation used", value=f"{ctx.author.name} has purged {amount} message(s)")
            log.set_footer(text="Bot provided by www.nootdev.dev", icon_url="https://cdn.discordapp.com/attachments/589652333638451211/796970752829685802/unknown.png")
            await channel.send(embed=log)
        else:
            em = discord.Embed(color=errorc)
            em.title = "Uh oh!"
            em.description = "An unknown error occured!"
            await ctx.send(embed=em)



    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member=None, reason="No reason specified"):
        db = await aiosqlite.connect("sql/main.sqlite")
        cursor = await db.execute(f"SELECT channel_id FROM logs WHERE guild_id = {ctx.guild.id}")
        result = await cursor.fetchone()
        await ctx.message.delete()
        if member is None:
            await ctx.message.delete()
            em = discord.Embed(color=color)
            em.title = "Kick command"
            em.description = ";Kick {member} {reason}"
            return await ctx.send(embed=em)
        elif result == None:
            await ctx.message.delete()
            dm = await member.create_dm()
            em = discord.Embed(color=color)
            em.description = "You have been kicked from **" + ctx.guild.name+ "** for **{}**" .format(reason)
            await dm.send(embed=em)
            embed = discord.Embed(color=donec)
            embed.description = f"Kicked {member.name}"
            await ctx.send(embed=embed)
            await ctx.guild.kick(user=member, reason=reason)
            return
        elif result is not None:
            await ctx.message.delete()
            dm = await member.create_dm()
            em = discord.Embed(color=color)
            em.description = "You have been banned from **" + ctx.guild.name+ "** for **{}**" .format(reason)
            await dm.send(embed=em)
            embed = discord.Embed(color=donec)
            embed.description = f"Banned {member.name}"
            await ctx.send(embed=embed)
            await ctx.guild.kick(user=member, reason=reason)
            channel = self.client.get_channel(int(result[0]))
            log = discord.Embed(color=color)
            log.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            log.add_field(name="Moderation used", value=f"{ctx.author.name} has kicked {member.name}")
            log.set_footer(text="Bot provided by www.nootdev.dev", icon_url="https://cdn.discordapp.com/attachments/589652333638451211/796970752829685802/unknown.png")
            await channel.send(embed=log)
        else:
            em = discord.Embed(color=errorc)
            em.title = "Uh oh!"
            em.description = "An unknown error occured!"
            await ctx.send(embed=em)



    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member=None, *, reason="No reason specified"):
        db = await aiosqlite.connect("sql/main.sqlite")
        cursor = await db.execute(f"SELECT channel_id FROM logs WHERE guild_id = {ctx.guild.id}")
        result = await cursor.fetchone()
        if member == None:
            em = discord.Embed(color=color)
            em.title = "Ban command"
            em.description = ";Ban {member} {reason}"
            return await ctx.send(embed=em)
        elif result == None:
            await ctx.message.delete()
            dm = await member.create_dm()
            em = discord.Embed(color=color)
            em.description = "You have been banned from **" + ctx.guild.name+ "** for **{}**" .format(reason)
            await dm.send(embed=em)
            embed = discord.Embed(color=donec)
            embed.description = f"Banned {member.name}"
            await ctx.send(embed=embed)
            await ctx.guild.ban(user=member, reason=reason)
            return
        elif result is not None:
            await ctx.message.delete()
            dm = await member.create_dm()
            em = discord.Embed(color=color)
            em.description = "You have been banned from **" + ctx.guild.name+ "** for **{}**" .format(reason)
            await dm.send(embed=em)
            embed = discord.Embed(color=donec)
            embed.description = f"Banned {member.name}"
            await ctx.send(embed=embed)
            await ctx.guild.ban(user=member, reason=reason)
            channel = self.client.get_channel(int(result[0]))
            log = discord.Embed(color=color)
            log.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            log.add_field(name="Moderation used", value=f"{ctx.author.name} has banned {member.name} who's ID is {member.id}")
            log.set_footer(text="Bot provided by www.nootdev.dev", icon_url="https://cdn.discordapp.com/attachments/589652333638451211/796970752829685802/unknown.png")
            await channel.send(embed=log)
        else:
            em = discord.Embed(color=errorc)
            em.title = "Uh oh!"
            em.description = "An unknown error occured!"
            await ctx.send(embed=em)



    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userid=None):
        db = await aiosqlite.connect("sql/main.sqlite")
        cursor = await db.execute(f"SELECT channel_id FROM logs WHERE guild_id = {ctx.guild.id}")
        result = await cursor.fetchone()
        if userid == None:
            em = discord.Embed(color=color)
            em.title = "Unban command"
            em.description = ";Unban {userid}"
            await ctx.send(embed=em)
        elif result == None:
            await ctx.message.delete()
            username = await self.client.fetch_user(int(userid))
            user = discord.Object(id=userid)
            await ctx.guild.unban(user)
            embed = discord.Embed(color=donec)
            embed.description = f"Unbanned {username}"
            await ctx.send(embed=embed)
        elif result is not None:
            await ctx.message.delete()
            username = await self.client.fetch_user(int(userid))
            user = discord.Object(id=userid)
            await ctx.guild.unban(user)
            embed = discord.Embed(color=donec)
            embed.description = f"Unbanned {username}"
            await ctx.send(embed=embed)
            channel = self.client.get_channel(int(result[0]))
            log = discord.Embed(color=color)
            log.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            log.add_field(name="Moderation used", value=f"{ctx.author.name} has unbanned {username}")
            log.set_footer(text="Bot provided by www.nootdev.dev", icon_url="https://cdn.discordapp.com/attachments/589652333638451211/796970752829685802/unknown.png")
            await channel.send(embed=log)
        else:
            em = discord.Embed(color=errorc)
            em.title = "Uh oh!"
            em.description = "An unknown error occured!"
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(Administrator(client))
    return