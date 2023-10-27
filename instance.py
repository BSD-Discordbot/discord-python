import os
import discord
from discord.ext import commands

from commands.pull import pull

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

bot.add_command(pull)

bot.run(os.getenv("DISCORD_TOKEN", ""))