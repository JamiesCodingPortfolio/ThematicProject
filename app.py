#Imports the bot from bot.py
from bot import *
#Logging import to log stuff and setup
import logging
logging.basicConfig(level=logging.INFO)
#For relative pathing for auth token
from pathlib import Path
#DiscordPy imports
import discord
from discord import app_commands
from discord.ext import commands
#imports other folders/dependencies
from adminCommands import *
from Commands import flashcardmaker
from Commands import hello
from variablesImport import BOT_TOKEN, ADMINCHANNEL
from commandImports import *

#error handling for if the token file is not found
if BOT_TOKEN == '':
    logging.error("Token file not found.")
    exit()

# Initializes the bot from the Client class

bot = Client()

#imports other commands from other files

#bot.add_command(runningCommand.runningbot)

#states that the bot is running, with the name of the device that is running is
        
#@bot.event
#async def on_message(message):
    #adminChannel = bot.get_channel(int(ADMINCHANNEL))
    #await adminChannel.send(message.content)
    

#implements an 'aboutcommands' command that lists all the bot commands and what they do in a Discord embed
@bot.command(help="Lists all the bot's commands and what they do")
async def aboutcommands(help):
    embed = discord.Embed(
        title="Boom Bot Commands List",
        description="Here are all the commands that I can perform:",
        color=discord.Color.red()
    )

    for command in bot.commands:
        embed.add_field(name=f"!{command.name}", value=command.help, inline=False)

    await help.send(embed=embed)

@bot.command(help="Shuts down the bot")
async def botshutdown(shutdown):
    await shutdown.send('Shutting down bot')
    await bot.close()

# Run the bot with your bot token
bot.run(BOT_TOKEN)