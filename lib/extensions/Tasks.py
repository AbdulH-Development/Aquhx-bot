import discord
import math
from discord.ext import commands
from discord.ext.commands import Cog


class handler(Cog):
    def __init__(self, client):
        self.client = client


    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)

        if isinstance(error, commands.ChannelNotFound):
            em = discord.Embed(color=0xff0000)
            em.description = 'Could not find that channel'
            await ctx.send(embed=em)
            return
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(color=0xff0000)
            em.description = 'The command you have attempted to execute is on cooldown.\nPlease try again in {}s.'.format(
                math.ceil(error.retry_after))
            await ctx.send(embed=em)
            return
        if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace(
                'guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                perms = '{}, and {}'.format(
                    "**, **".join(missing[:-1]), missing[-1])
            else:
                perms = ' and '.join(missing)
            em = discord.Embed(color=0xff0000)
            em.description = 'You do not have the the **{}** permission(s) which is needed to execute the command'.format(
                perms)
            await ctx.send(embed=em)
            return
        if isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace(
                'guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                perms = '{}, and {}'.format(
                    "**, **".join(missing[:-1]), missing[-1])
            else:
                perms = ' and '.join(missing)
            em = discord.Embed(color=0xff0000)
            em.description = "[ERROR] I am missing the **{}** permission(s) to execute the command".format(
                perms)
            await ctx.send(embed=em)
            return
        if isinstance(error, commands.CommandNotFound):
            em = discord.Embed(color=0xff0000)
            em.description = "[ERROR] Unknown command"
            await ctx.send(embed=em)
            return


    @Cog.listener()
    async def on_error(self, ctx, error):
        if hasattr(ctx.command, 'on_command_error'):
            return

        error = getattr(error, 'original', error)

        if isinstance(error, KeyboardInterrupt):
            print("[ERROR] Program terminated by user")



def setup(client):
    client.add_cog(handler(client))
