import discord
from discord import app_commands
from discord.ext import commands

class remove_messages(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    # Define a slash command to remove messages
    @app_commands.command(name="remove_messages", description="Removes a specific number of messages from the channel (admin/mod only)")
    async def remove_messages(self, interaction: discord.Interaction, number: int): 

        # Defer the interaction to indicate the bot has received it and is working
        await interaction.response.defer()

        # Check if the user has permission to manage messages
        if not interaction.user.permissions_in(interaction.channel).manage_messages:
            await interaction.followup.send("You don't have permission to manage messages.", ephemeral=True)
            return

        # Check if the provided number is greater than zero. If not, send an error message and terminate the command
        if number <= 0:
            await interaction.response.send_message("Please provide a positive number greater than zero.", ephemeral=True)
            return
        
        try:
            # Attempt to delete the specified number of messages plus the command message itself
            await interaction.channel.purge(limit=number+1)

        # Include an except block to handle exceptions
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to delete messages.", ephemeral=True)

        except discord.HTTPException:
            await interaction.followup.send("An error occurred while attempting to delete the messages.", ephemeral=True)

# Define a setup function to add the cog to the bot 
async def setup(client: commands.Bot) -> None:
    await client.add_cog(remove_messages(client))
