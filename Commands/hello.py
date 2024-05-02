import discord
from discord import app_commands
from discord.ext import commands
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import dbAccess


class hello(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @app_commands.command(name="hello", description="Says Hello!")
    async def hello(self, interaction: discord.Interaction): 
        if (dbAccess.checkIfCommandIsActive(interaction.guild_id, 'Commands', 'hello') == True):
            await interaction.response.send_message(content=f"Hello {interaction.user.mention}!" , ephemeral=True)
        
        else:
            await interaction.response.send_message("This command currently isn't active in this server. Ask the admin to activate it.", ephemeral=True)
            return
async def setup(client:commands.Bot) -> None:
    await client.add_cog(hello(client))