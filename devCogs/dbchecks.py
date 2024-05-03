import sys
import os
import json
import discord
from discord import app_commands
from discord.ext import commands
import socket
from colorama import Fore

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory by going one level up
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to sys.path
sys.path.append(parent_dir)

from variablesImport import ADMINSERVER
from bot import prfx
import dbAccess

class dbcheck(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    adminserver = int(ADMINSERVER)
    @app_commands.command(name="dbcheck", description="Checks if default commands match the current JsonExample file.")
    @app_commands.guilds(discord.Object(id=adminserver))
    async def dbcheck(self, interaction: discord.Interaction) -> None: 
        response = dbAccess.dbUpdate(ADMINSERVER)
        await interaction.response.send_message(content=response)
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        try:
            dbAccess.createServerInDatabase(guild.id)  # Create server in database if it isn't already present.
        except discord.HTTPException as e:
            print(f"Error running dbcheck for guild {guild.id}: {e}")  # Handle potential errors
            
async def setup(client:commands.Bot) -> None:
    await client.add_cog(dbcheck(client))
    #server_ids = [1210173480344092674]
    #for guild_id in server_ids:
        #guild = client.get_guild(guild_id)  # Get guild object
        #if guild:
            #await client.tree.sync(guild=discord.Object(id=guild))  # Sync for specific guild
    await client.tree.sync(guild=discord.Object(id=ADMINSERVER))
    print(prfx + " Db checks synced ")