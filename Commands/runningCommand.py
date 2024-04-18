import discord
from discord.ext import commands

import socket

@commands.command(help="Displays what PC is currently running the bot process")
async def runningbot(runBot):
    await runBot.send('The PC currently running this bot is ' + socket.gethostname())