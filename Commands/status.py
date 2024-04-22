import sys
import os
import discord
from discord import app_commands
from discord.ext import commands
import socket

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory by going one level up
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to sys.path
sys.path.append(parent_dir)

from variablesImport import ADMINSERVER



class status(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    adminserver = int(ADMINSERVER)
    @app_commands.command(name="status", description="Displays the status of the bot")
    @app_commands.guilds(discord.Object(id=adminserver))
    async def status(self, interaction: discord.Interaction) -> None: 
        await interaction.response.send_message(content='The PC currently running this bot is ' + socket.gethostname())
    
async def setup(client:commands.Bot) -> None:
    await client.add_cog(status(client))
    await client.tree.sync(guild=discord.Object(id=status.adminserver))
    print("status synced")