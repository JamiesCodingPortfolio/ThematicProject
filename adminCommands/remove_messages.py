import discord
from discord import app_commands
from discord.ext import commands

class remove_messages(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    # Define a slash command to remove messages
    @app_commands.command(name="removeMessages", description="Removes a specific number of messages from the channel")

    # Check if the user has manage_messages permission
    @commands.has_permissions(manage_messages=True)
    
    async def remove_messages(self, interaction: discord.Interaction, number: int): 

        # Check if the provided number is greater than zero. If not, send an error message and terminate the command
        if number <= 0:
            await interaction.response.send_message(content="Please provide a positive number greater than zero.", ephemeral=True)
            return
        
        try:
            # Attempt to delete the specified number of messages plus the command message itself
            await interaction.channel.purge(limit=number + 1)

            # Send a confirmation message that the number of messages have been deleted from the same channel
            await interaction.response.send_message(content=f"Successfully removed {number} messages.", ephemeral=True)

        # Include an except block to send an error message where the bot doesn't have permission to delete messages
        except discord.Forbidden:
            await interaction.response.send_message(content="I don't have permission to delete messages.", ephemeral=True)

# Define a setup function to add the cog to the bot 
async def setup(client:commands.Bot) -> None:
    await client.add_cog(remove_messages(client))