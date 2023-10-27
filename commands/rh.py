from discord.ext import commands
from discord.ext.commands.context import Context
from database_utils import get_db, get_player


@commands.command()
async def rh(ctx: Context, db=get_db()):
    player = get_player(db, str(ctx.author.id))
    if player.daily_streak < 7:
        return await ctx.send("Votre combo journalier n'est pas suffisant. Requis : 7")
    player.balance += 500
    player.daily_streak = 0
    db.commit()
    db.refresh(player)
    await ctx.send(player.balance)
