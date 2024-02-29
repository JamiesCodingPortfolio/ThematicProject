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
import commands

#grabs discord bot token from text file
desktop_path = Path.home() / "Desktop"

token_file_path = desktop_path / "Bot token.txt"

if not token_file_path.is_file():
    logging.error("Token file not found on the desktop.")
    exit()

with open(token_file_path, 'r') as file:
    bot_token = file.read()

# Define the intents your client will use
intents = discord.Intents.all()
#intents.messages = True  # Enable the ability to receive message events

# Initialize the Client object with the defined intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.command(help="Says hello back to whoever said hello")
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')



@bot.command(help="Lists all the bot's commands and what they do")
async def aboutcommands(ctx):
    embed = discord.Embed(
        title="Empowerment Bot Commands List",
        description="Here are all the commands that I can perform:",
        color=discord.Color.red()
    )

    for command in bot.commands:
        embed.add_field(name=f"!{command.name}", value=command.help, inline=False)

    await ctx.send(embed=embed)

@bot.command(help="displays what PC is currently running the bot process")
async def runningbot(ctx):
    await ctx.send('The PC currently running this bot is ' + socket.gethostname())


# Run the bot with your bot token
bot.run(bot_token)