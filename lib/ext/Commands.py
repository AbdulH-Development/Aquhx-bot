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
import time
import asyncpg
import os
from dotenv import load_dotenv
import asyncio
import psycopg2
import praw
import random
import requests
import json
from random import randint
from typing import List, Union
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from discord_slash import SlashCommand
from ..bot.info import *


color = 0xfffafa  # 0xff4500  # 0x4B0082

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def invite(self, ctx):
        em = discord.Embed(color=self.client.color)
        em.title = "You seem to be enjoying the bot!"
        em.description = "Please invite the bot if you like it!\n**[Link](https://discord.com/oauth2/authorize?client_id=796594693865078825&permissions=3728076022&scope=bot)**"
        await ctx.send(embed=em)

    @commands.command(aliases=['meme'])
    @commands.cooldown(1, 10, BucketType.user)
    async def memes(self, ctx):
        subreddit = reddit.subreddit("memes")
        all_subs = []
        hot = subreddit.hot(limit=15)

        for submission in hot:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        embed = discord.Embed(title=random_sub.title,
                              colour=randint(0, 0xffffff), url=random_sub.url)

        embed.set_author(
            name=f'Posted by {random_sub.author} from r/{random_sub.subreddit}')
        embed.set_image(url=random_sub.url)
        embed.set_footer(
            text=f'\t💬 {len(random_sub.comments)}         ⬆️ {random_sub.upvote_ratio}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['puppy', 'dogs'])
    @commands.cooldown(1, 10, BucketType.user)
    async def dog(self, ctx):
        subreddit = reddit.subreddit("puppies")
        all_subs = []
        hot = subreddit.hot(limit=15)

        for submission in hot:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        embed = discord.Embed(title=random_sub.title,
                              colour=randint(0, 0xffffff), url=random_sub.url)

        embed.set_author(
            name=f'Posted by {random_sub.author} from r/{random_sub.subreddit}')
        embed.set_image(url=random_sub.url)
        embed.set_footer(
            text=f'\t💬 {len(random_sub.comments)}         ⬆️ {random_sub.upvote_ratio}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['cat', 'cats'])
    @commands.cooldown(1, 10, BucketType.user)
    async def kitten(self, ctx):
        subreddit = reddit.subreddit("kittens")
        all_subs = []
        hot = subreddit.hot(limit=15)

        for submission in hot:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        embed = discord.Embed(title=random_sub.title,
                              colour=randint(0, 0xffffff), url=random_sub.url)

        embed.set_author(
            name=f'Posted by {random_sub.author} from r/{random_sub.subreddit}')
        embed.set_image(url=random_sub.url)
        embed.set_footer(
            text=f'\t💬 {len(random_sub.comments)}         ⬆️ {random_sub.upvote_ratio}')
        await ctx.send(embed=embed)

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
            await ctx.message.delete()
            if "@everyone" in words:
                return
            if "@here" in words:
                return
            else:
                await ctx.send("{}" .format(words))


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
            await ctx.message.delete()
            if "@here" in words:
                return
            elif "@everyone" in words:
                return
            else:
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
        em1 = discord.Embed(color=color)
        em1.set_author(icon_url=self.client.user.avatar_url,
                       name="Cairo moderation list")

        em1.add_field(name="Ban", value="Ban a member")
        em1.add_field(name="Unban", value="Unban a user")
        em1.add_field(name="Kick", value="Kick a member")
        em1.add_field(name="Mute", value="Mute a member")
        em1.add_field(name="Unmute", value="Unmute a member")
        em1.add_field(name="Clear", value="Purge some messages")
        em1.add_field(name="Setup", value="Setup some per server stuff")
        em1.add_field(name="Prefix", value="Set a custom prefix")
        em1.add_field(name="Logs", value="Set up your logging channel")
        em1.add_field(name="Welcome", value="Set up your welcome message")
        em1.add_field(name="Goodbye", value="Set up your goodbye message")
        em1.add_field(name="Welchan", value="Set up your Welcome channel")
        em1.add_field(name="Goodchan", value="Set up your goodbye channel")
        em1.add_field(name="Remwel", value="Remove every welcome item in the database")
        em1.add_field(name="Remgood", value="Remove every goodbye items in the database")
        em1.add_field(name="Remlogs", value="Remove your logs channel from the database")
        em1.set_footer(
            text=f"Requested by {ctx.author.name} at {current_time}", icon_url=ctx.author.avatar_url)

        em3 = discord.Embed(color=color)
        em3.set_author(icon_url=self.client.user.avatar_url,
                       name="Cairo command list")
        em3.add_field(name="Say", value="Say something")
        em3.add_field(name="Embed", value="Embed something")
        em3.add_field(name="Poll", value="Vote on something")
        em3.add_field(name="Memes", value="Get memes from reddit!")
        em3.add_field(name="Kitten", value="Get pictures of adorable kittens!")
        em3.add_field(name="Puppy", value="Get pictures of adorable puppies!")
        em3.add_field(name="Invite", value="Invite the bot!")
        em3.set_footer(
            text=f"Requested by {ctx.author.name} at {current_time}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=em3)
        await msg.add_reaction('◀️')
        await msg.add_reaction('▶️')
        await msg.add_reaction('🗑️')

        def reac_check(r, u):
            return u == ctx.author and msg.id == r.message.id and u != self.client.user and r.emoji in ['◀️', '▶️', '🗑️']

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

            if em == '◀️':
                await msg.edit(embed=em3)

            if em == '▶️':
                await msg.edit(embed=em1)

            if em == "🗑️":
                await msg.delete()
                await ctx.message.delete()


def setup(client):
    client.add_cog(Fun(client))