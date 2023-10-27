import os
import discord
from commands.pull import pull
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(intents=intents)
bot.add_command(pull)
bot.run(os.getenv("DISCORD_TOKEN", ""))