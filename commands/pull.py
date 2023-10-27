from discord.ext import commands

@commands.command()
async def pull(ctx, arg):
    await ctx.send(arg)