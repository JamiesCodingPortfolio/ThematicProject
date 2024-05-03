import discord
from discord import app_commands
from discord.ext import commands
import sys
import os
import random

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import dbAccess

class numbergenerator(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @app_commands.command(name="numbergenerator", description="Chooses a random number between 1 and 2!")
    async def numbergenerator(self, interaction: discord.Interaction):
        if dbAccess.checkIfCommandIsActive(interaction.guild_id, 'Commands', 'numbergenerator'):
            number = random(1,2)
            await interaction.response.send_message(content=f"Hello {interaction.user.mention} the number that has been generated is {number}!")
        else:
            await interaction.response.send_message(content="This command currently isn't active in this server. Ask the admin to activate it.", ephemeral=True)
        
async def setup(client:commands.Bot) -> None:
    await client.add_cog(numbergenerator(client))