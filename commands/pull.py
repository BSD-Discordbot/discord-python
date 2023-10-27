from io import BytesIO
from math import floor
import random
from discord import File
from discord.ext import commands
from discord.ext.commands.context import Context
from database_utils import get_db, get_player
import sqlalchemy as sa
from sqlalchemy.sql.expression import func
from db import models
from PIL import Image

def randomToRarity(r: float):
    return 1 if r < 2 / 3 else 2 if r < 13 / 15 else 3 if r < 49 / 50 else 4


def randomCardFromRarity(r: int):
    return (
        get_db()
        .query(models.Card)
        .where(models.Card.rarity == r)
        .order_by(func.random())
        .limit(1)
        .first()
    )

def generateImage(cards: list[models.Card]):
    nmbWidth = cards.__len__()
    atlas = Image.new('RGBA', (nmbWidth*(288+50), 1*450+50))
    for index, card in enumerate(cards):
        if(card.image != None):
            x = (index%nmbWidth)*(288+50)+25
            y = (floor(index/nmbWidth))*450+25
            img = Image.open(BytesIO(card.image)).resize((288, 450))
            atlas.paste(img, (x, y, x+288, y+450))
    return atlas


@commands.command()
async def pull(ctx: Context, db=get_db()):
    player = get_player(db, str(ctx.author.id))
    if player.balance < 200:
        return await ctx.send("Vous n'avez pas les fonds nécessaires. Requis : 200")
    player.balance -= 200
    cards = [randomCardFromRarity(randomToRarity(random.random())) for x in range(5)]
    for card in cards:
        duplicate = next((c for c in player.card_ownership if c.card_id == card.id), None)
        if(duplicate != None):
            duplicate.amount += 1
        else:
            ownership = models.CardOwnership(player=player, card_id=card.id, amount=1)
            player.card_ownership.append(ownership)       
    db.commit()
    db.refresh(player)
    temp_io = BytesIO()
    generateImage(cards).save(temp_io, format="PNG")
    temp_io.seek(0)
    await ctx.send(file = File(temp_io, 'pull.png'))