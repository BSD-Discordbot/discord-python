import os
import discord
from commands.pull import pull
from commands.rj import rj
from commands.rh import rh
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)

bot.add_command(pull)
bot.add_command(rj)
bot.add_command(rh)

bot.run(os.getenv("DISCORD_TOKEN", ""))
