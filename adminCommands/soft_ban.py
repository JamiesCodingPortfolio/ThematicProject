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
    async def soft_ban(self, ctx, member: discord.Member, hours: int, minutes: int, reason: str = None): 
        print("Soft ban command received.")
        if dbAccess.checkIfCommandIsActive(ctx.guild.id, 'adminCommands', 'soft_ban'):
            print("Soft ban command is active.")

            # Check if the command is invoked by a message or a slash command
            if isinstance(ctx, commands.Context):
                # For message commands
                author_id = ctx.author.id
            elif isinstance(ctx, discord.Interaction):
                # For slash commands
                author_id = ctx.user.id
            else:
                # Unsupported context type
                return

            # Check if the user invoking the command is the owner
            if author_id == ctx.guild.owner_id:
                if member == ctx.author:
                    await ctx.send("You can't ban yourself.")
                    return
                await self.perform_soft_ban(ctx, member, hours, minutes, reason)
                return

            # Check if the target user is the owner
            if member == ctx.guild.owner:
                await ctx.send("You can't ban the server owner.")
                return

            # Check if the user invoking the command has the necessary permissions
            if isinstance(ctx, commands.Context) and not ctx.author.guild_permissions.ban_members:
                await ctx.send("You don't have permission to ban members.")
                return

            # Check if the user has a lower role than the target user
            if ctx.guild.get_member(author_id).top_role <= member.top_role:
                await ctx.send("You can't ban someone with a higher or equal role.")
                return

            # Perform the soft ban
            await self.perform_soft_ban(ctx, member, hours, minutes, reason)
        else:
            print("Soft ban command is not active.")


    async def perform_soft_ban(self, ctx, member: discord.Member, hours: int, minutes: int, reason: str):
        print("Performing soft ban.")
        try:
            # Send a DM to the banned user
            try:
                invite = await ctx.channel.create_invite()
                ban_message = f"You have been banned from {ctx.guild.name} for {hours} hours and {minutes} minutes. Reason: {reason}\n\nYou can rejoin once unbanned using this invite link: {invite}"
                await member.send(ban_message)
            except discord.Forbidden as e:
                await ctx.send(f"I couldn't send a DM to {member.display_name}: {e}")
                return

            # Concurrently purge all messages from the user in the entire server before banning
            await asyncio.gather(
                self.purge_messages(ctx.guild, member),
                self.ban_user(member, hours, minutes, reason)
            )

        except discord.Forbidden as e:
            await ctx.send(f"I don't have permission to ban members: {e}")

        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while attempting to ban the member: {e}")


    async def purge_messages(self, guild, member):
        print("Purging messages.")
        # Purge all messages from the user in the entire server
        for channel in guild.text_channels:
            await channel.purge(limit=None, check=lambda m: m.author == member)


    async def ban_user(self, member: discord.Member, hours: int, minutes: int, reason: str):
        print("Banning user.")
        # Ban the user with the reason stated
        await member.ban(reason=reason)

        # Define an editable placeholder for the ban confirmation message
        ban_confirmation_message = f"{member.display_name} has been banned for {hours} hours and {minutes} minutes. Reason: {reason}"
        message = await member.guild.system_channel.send(ban_confirmation_message)

        # Schedule the unban
        unban_time = datetime.datetime.now() + datetime.timedelta(hours=hours, minutes=minutes)

        # Edit the message placeholder with the time until the user is unbanned
        while datetime.datetime.now() < unban_time:
            remaining_time = unban_time - datetime.datetime.now()
            remaining_time_str = f"{remaining_time.seconds // 3600}h {remaining_time.seconds % 3600 // 60}m {remaining_time.seconds % 60}s"
            await message.edit(content=f"{ban_confirmation_message}\nTime remaining: {remaining_time_str}")
            await asyncio.sleep(1)  # Update every second

        # Once the unban time comes, state that the soft ban has expired
        await member.guild.unban(member, reason="Soft ban expired.")

        # Send a message when the user is unbanned
        await member.guild.system_channel.send(f"{member.display_name} has been unbanned after {hours} hours and {minutes} minutes.")

# Define a setup function to add the cog to the bot 
async def setup(client: commands.Bot) -> None:
    await client.add_cog(soft_ban(client))
