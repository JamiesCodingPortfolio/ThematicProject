#Logging import to log stuff and setup
import logging
logging.basicConfig(level=logging.INFO)
#For relative pathing for auth token
from pathlib import Path
#DiscordPy imports
import discord
from discord.ext import commands
#To grab whoever is running the bot
import socket
#imports other folders/dependencies
from adminCommands import *
from Commands import flashcardmaker
from Commands import *
from variablesImport import BOT_TOKEN, ADMINCHANNEL
from commandImports import *

#error handling for if the token file is not found
if BOT_TOKEN == '':
    logging.error("Token file not found.")
    exit()

# Define the intents your client will use
intents = discord.Intents.all()

# Initialize the Client object with the defined intents
bot = commands.Bot(command_prefix='!', intents=intents)

#imports other commands from other files
bot.add_command(flashcardmaker.makeflashcard)
bot.add_command(flashcardmaker.defineflashcard)
bot.add_command(flashcardmaker.deleteflashcard)
#bot.add_command(runningCommand.runningbot)

#states that the bot is running, with the name of the device that is running is

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    adminChannel = bot.get_channel(int(ADMINCHANNEL))
    if adminChannel is not None:
        await adminChannel.send('The bot is running and the PC currently running this bot is ' + socket.gethostname())
    else:
        print("Channel not found.")
        
#@bot.event
#async def on_message(message):
    #adminChannel = bot.get_channel(int(ADMINCHANNEL))
    #await adminChannel.send(message.content)
    

#implements a 'hello' command that says hello back to whoever said it
@bot.command(help="Says hello back to whoever said hello")
async def hello(hello):
    await hello.send(f'Hello {hello.author.mention}!')


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

#implements a 'runningbot' command that states the bot is running, with the device it is running on
@bot.command(help="Displays what PC is currently running the bot process")
async def runningbot(runBot):
    await runBot.send('The PC currently running this bot is ' + socket.gethostname())

@bot.command(help="Shuts down the bot")
async def botshutdown(shutdown):
    await shutdown.send('Shutting down bot')
    await bot.close()

# Run the bot with your bot token
bot.run(BOT_TOKEN)