import discord
from discord import app_commands
from discord.ext import commands

@bot.command(help="Shuts down the bot")
async def botshutdown(shutdown):
    await shutdown.send('Shutting down bot')
    await bot.close()