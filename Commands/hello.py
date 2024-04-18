import discord
from discord import app_commands
from discord.ext import commands

class hello(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @app_commands.command(name="hello", description="Says Hello!")
    async def hello(self, interaction: discord.Interaction): 
        await interaction.response.send_message(content=f"Hello {interaction.user.mention}!" , ephemeral=True)
        
async def setup(client:commands.Bot) -> None:
    await client.add_cog(hello(client))