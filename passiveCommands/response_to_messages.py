import discord
from discord import app_commands
from discord.ext import commands
from fuzzywuzzy import fuzz  # Import the fuzz function from fuzzywuzzy for partial string matching

class response_to_messages(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.responses = {}
        
    # Define a slash command to add responses to certain messages
    @app_commands.command(name="add_response_to_message", description="Causes the bot to respond to specific messages with certain words or images.")
    async def add_response(self, interaction: discord.Interaction, message: str, response: str): 

        # Check if the user is an administrator
        if not interaction.author.guild_permissions.manage_messages and not interaction.author.guild_permissions.administrator:
            await interaction.response.send_message(content="You don't have permission to use this command.", ephemeral=True)
            return
        
        try:
            # Add the response for the trigger message
            self.responses[message.lower()] = response
            await interaction.response.send_message(f"Response added for trigger '{message}': '{response}'", ephemeral=True)

        # Include an except block to handle exceptions
        except discord.Forbidden:
            await interaction.response.send_message(content="I don't have permission to add responses.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(content=f"An error occurred: {e}", ephemeral=True)


    # Listen for messages and respond with the responses defined in the dictionary
    @commands.Cog.listener()
    async def on_message(self, message):

        # Ignore if the message was sent by the bot itself
        if message.author == self.client.user:
            return
    
        # Check if the message partially matches any trigger and give the appropriate response if so
        for trigger, response in self.responses.items():
            if fuzz.partial_ratio(trigger.lower(), message.content.lower()) >= 40:
                await message.channel.send(response, ephemeral=True)
                break

# Define a setup function to add the cog to the bot 
async def setup(client: commands.Bot) -> None:
    await client.add_cog(response_to_messages(client))
