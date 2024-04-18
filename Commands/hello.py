import discord
from discord import app_commands
from discord.ext import commands

class hello(commands.GroupCog):
    def __init__(self, client):
        self.client=client
        
    @app_commands.command(name="hello")
    async def hello(self, interaction: discord.Interaction): 
        await interaction.response.send_message(f"Hello {interaction.user.mention}!" , ephemeral=True)
        
async def setup(client):
    await client.add_cog(hello(client))
    
    