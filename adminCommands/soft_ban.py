import discord
from discord import app_commands
from discord.ext import commands
import datetime
import asyncio

class soft_ban(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @app_commands.command(name="soft_ban", description="Bans a user temporarily, also deleting all their messages (admin/mod only)")
    async def soft_ban(self, interaction: discord.Interaction, member: discord.Member, hours: int, minutes: int, reason: str = None): 
        # Defer the interaction to indicate the bot has received it and is working
        await interaction.response.defer()

        # Check if the user has permission to ban members. If not, tell them they don't have permission
        if not interaction.user.permissions_in(interaction.channel).ban_members:
            await interaction.followup.send("You don't have permission to ban members.", ephemeral=True)
            return

        try:
            # Calculate the duration of the ban based on the hours and minutes entered
            ban_duration = datetime.timedelta(hours=hours, minutes=minutes)

            # Ban the user with the reason stated
            await member.ban(reason=reason)
            
            # Purge all messages from the user in the entire server
            for guild in self.client.guilds:
                for channel in guild.text_channels:
                    await channel.purge(limit=None, check=lambda m: m.author == member)
            
            # Schedule the unban
            await asyncio.sleep(ban_duration.total_seconds())

            # Once the unban time comes, state that the soft ban has expired
            await member.unban(reason="Soft ban expired.")

            # Send a confirmation message for the ban with the time and reason
            await interaction.followup.send(f"{member.display_name} has been banned for {hours} hours and {minutes} minutes. Reason: {reason}", ephemeral=True)
        
        # Include an except block to handle exceptions
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to ban members.", ephemeral=True)
        
        except discord.HTTPException:
            await interaction.followup.send("An error occurred while attempting to ban the member.", ephemeral=True)

# Define a setup function to add the cog to the bot 
async def setup(client: commands.Bot) -> None:
    await client.add_cog(soft_ban(client))
