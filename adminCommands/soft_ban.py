import sys
import os
import discord
from discord import app_commands
from discord.ext import commands
import datetime
import asyncio

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import dbAccess

class soft_ban(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        
    @app_commands.command(name="soft_ban", description="Bans a user temporarily, also deleting all their messages (admin/mod only)")
    async def soft_ban(self, interaction: discord.Interaction, member: discord.Member, hours: int, minutes: int, reason: str = None): 
        if (dbAccess.checkIfCommandIsActive(interaction.guild_id, 'adminCommands', 'soft_ban') == True):
            # Defer the interaction to indicate the bot has received it and is working
            await interaction.response.defer()

            # Check if the user invoking the command is the owner. If it is, let them perform a soft ban
            if interaction.user.id == interaction.guild.owner_id:
                await self.perform_soft_ban(interaction, member, hours, minutes, reason)
                return

            # Check if the target user is the owner. If it is, tell the person invoking that they can't ban the owner
            if member == interaction.guild.owner:
                await interaction.followup.send("You can't ban the server owner.", ephemeral=True)
                return

            # Check if the user invoking the command is an admin or mod. If they are, let them perform a soft ban
            if interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.ban_members:
                await self.perform_soft_ban(interaction, member, hours, minutes, reason)
                return

            # If the user doesn't have permissions to ban members, tell them this
            await interaction.followup.send("You don't have permission to ban members.", ephemeral=True)
            
            
        else:
            await interaction.response.send_message("This command currently isn't active in your server. You can activate it from the bot dashboard.", ephemeral=True)
            return

    async def perform_soft_ban(self, interaction: discord.Interaction, member: discord.Member, hours: int, minutes: int, reason: str):
        try:
            # Send a DM to the banned user
            try:
                invite = await interaction.channel.create_invite()
                ban_message = f"You have been banned from {interaction.guild.name} for {hours} hours and {minutes} minutes. Reason: {reason}\n\nYou can rejoin once unbanned using this invite link: {invite}"
                await member.send(ban_message)
            except discord.Forbidden as e:
                await interaction.followup.send(f"I couldn't send a DM to {member.display_name}: {e}", ephemeral=True)
                return
            
            # Purge all messages from the user in the entire server
            for guild in self.client.guilds:
                for channel in guild.text_channels:
                    await channel.purge(limit=None, check=lambda m: m.author == member or m.reference and m.reference.author == member)
            
            # Schedule the unban
            await asyncio.sleep(ban_duration.total_seconds())

            # Once the unban time comes, state that the soft ban has expired
            await member.unban(reason="Soft ban expired.")

            # Send a confirmation message for the ban with the time and reason
            await interaction.followup.send(f"{member.display_name} has been banned for {hours} hours and {minutes} minutes. Reason: {reason}", ephemeral=True)
        
        # Include an except block to handle exceptions
        except discord.Forbidden as e:
            await interaction.followup.send(f"I don't have permission to ban members: {e}", ephemeral=True)
        
        except discord.HTTPException as e:
            await interaction.followup.send(f"An error occurred while attempting to ban the member: {e}", ephemeral=True)

# Define a setup function to add the cog to the bot 
async def setup(client: commands.Bot) -> None:
    await client.add_cog(soft_ban(client))