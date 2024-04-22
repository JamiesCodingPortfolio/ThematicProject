import discord
from discord import app_commands
from discord.ext import commands

class remove_messages(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    # Define a slash command to remove messages
    @app_commands.command(name="remove_messages", description="Removes a specific number of messages from the channel")
    async def remove_messages(self, interaction: discord.Interaction, number: int): 

        # Defer the interaction first
        await interaction.response.defer()

        # Check if the provided number is greater than zero. If not, send an error message and terminate the command
        if number <= 0:
            await interaction.followup.send(content="Please provide a positive number greater than zero.", ephemeral=True)
            return
        
        try:
            # Attempt to delete the specified number of messages plus the command message itself
            deleted = await interaction.channel.purge(limit=number)
            
            # Check if messages were deleted successfully
            if len(deleted) == number:
                # Send a confirmation message that the number of messages have been deleted from the same channel
                await interaction.followup.send(content=f"Successfully removed {number} messages.", ephemeral=True)

            else:
                await interaction.followup.send(content="Failed to remove messages. Please make sure I have permission to delete messages.", ephemeral=True)

        # Include an except block to handle exceptions
        except discord.Forbidden:
            await interaction.followup.send(content="I don't have permission to delete messages.", ephemeral=True)

# Define a setup function to add the cog to the bot 
async def setup(client:commands.Bot) -> None:
    await client.add_cog(remove_messages(client))
