import discord
from discord import app_commands
from discord.ext import commands

class ban(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @app_commands.command(name="ban", description="Bans a user (admin/mod only)")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason=None): 
        # Defer the interaction to indicate the bot has received it and is working
        await interaction.response.defer()

        # Check if the user has permission to ban members
        if not interaction.user.permissions_in(interaction.channel).ban_members:
            await interaction.followup.send("You don't have permission to ban members.", ephemeral=True)
            return

        try:
            await member.ban(reason=reason)
            await interaction.followup.send(f"{member.display_name} has been banned.", ephemeral=True)
        
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to ban members.", ephemeral=True)
        
        except discord.HTTPException:
            await interaction.followup.send("An error occurred while attempting to ban the member.", ephemeral=True)

# Define a setup function to add the cog to the bot 
async def setup(client: commands.Bot) -> None:
    await client.add_cog(ban(client))
