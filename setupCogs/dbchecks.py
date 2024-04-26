import sys
import os
import json
import discord
from discord import app_commands
from discord.ext import commands
import socket
from colorama import Fore
from bot import prfx
import dbAccess

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory by going one level up
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to sys.path
sys.path.append(parent_dir)

from variablesImport import ADMINSERVER

class dbcheck(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.db = dbAccess.db
        
    adminserver = int(ADMINSERVER)
    @app_commands.command(name="dbcheck", description="Checks if default commands match the current JsonExample file.")
    @app_commands.guilds(discord.Object(id=adminserver))
    async def dbcheck(self, interaction: discord.Interaction) -> None: 
        json_example_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "JsonExample.json")
        mismatched_servers = []  # Empty list to store server IDs with mismatches
        with open(json_example_path, 'r') as json_file:
            json_data = json.load(json_file)
            
        for guild in self.client.guilds:
            server_id = str(guild.id)
            existing_document = self.db["servers"].find_one({'ServerID': server_id})
            
            if 'DefaultCommands' in existing_document and 'DefaultCommands' in json_data:
                if existing_document['DefaultCommands'] != json_data['DefaultCommands']:
                    mismatched_servers.append(server_id)  # Add server ID to list

        if mismatched_servers:  # Check if there are mismatches
            message = "Documents for the following servers do not match JsonExample:\n" + ", ".join(mismatched_servers) + "\nConsider updating the documents or JsonExample."
            await interaction.response.send_message(content=message)
        else:
            await interaction.response.send_message(content="JSON Data matches what is currently within Database when compared to JsonExample.")
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            await self.dbcheck(guild)  # Call the dbcheck function with the joined guild
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
    print(prfx + " db checks synced ")