import discord
from discord import app_commands
from discord.ext import commands
import datetime
import asyncio
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import dbAccess

class timeout(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="timeout", description="Temporarily mutes a user.")
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, hours: int, minutes: int, reason: str = None):
        if (dbAccess.checkIfCommandIsActive(interaction.guild_id, 'Commands', 'hello') == True):
            await interaction.response.defer()

            if interaction.user.guild_permissions.ban_members:
                await interaction.followup.send(f"{member.display_name} has been timed out for {hours} hours and {minutes} minutes and will not be able to send messages. Reason: {reason}", ephemeral=True)
                await self.Timeout(interaction.guild, interaction, member, hours, minutes, reason)
                return

            if member.guild_permissions == interaction.user.guild_permissions.ban_members:
                await interaction.followup.send("You cannot timeout this member.", ephemeral=True)
                return

            await interaction.followup.send("You don't have permission to timeout members.", ephemeral=True)
        else:
            await interaction.response.send_message("This command currently isn't active in this server. Ask the admin to activate it.", ephemeral=True)
            return
        
    async def Timeout(self, guild: discord.Guild, interaction: discord.Interaction, member: discord.Member, hours: int, minutes: int, reason):
        try:
            duration = datetime.timedelta(hours=hours, minutes=minutes)

            for channel in guild.text_channels:
                overwrites = channel.overwrites_for(member)
                overwrites.send_messages = False  # Deny send_messages permission
                await channel.set_permissions(member, overwrite=overwrites)

            await asyncio.sleep(duration.total_seconds())

            for channel in guild.text_channels:
                overwrites = channel.overwrites_for(member)
                overwrites.send_messages = None  # Restore send_messages permission
                await channel.set_permissions(member, overwrite=overwrites)

        except discord.Forbidden:
            await interaction.followup.send("An error occured, check bot permissions.", ephemeral=True)

        except discord.HTTPException:
            await interaction.followup.send("An error occurred whilst connecting to the server.", ephemeral=True)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(timeout(client))
