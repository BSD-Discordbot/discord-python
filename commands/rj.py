from datetime import datetime, timedelta
from discord.ext import commands
from discord.ext.commands.context import Context
from database_utils import get_db, get_player


@commands.command()
async def rj(ctx: Context, db=get_db()):
    player = get_player(db, str(ctx.author.id))
    if player.last_daily > datetime.now() - timedelta(1):
        return await ctx.send(
            "Vous devez attendre encore "
            + str(
                round(
                    (
                        player.last_daily - (datetime.now() - timedelta(1))
                    ).total_seconds()
                    / 3600.0
                )
            )
            + " heures avant de pouvoir exécuter cette commande"
        )
    player.balance += 100
    player.last_daily = datetime.now()
    player.daily_streak += 1
    db.commit()
    db.refresh(player)
    await ctx.send(player.balance)
