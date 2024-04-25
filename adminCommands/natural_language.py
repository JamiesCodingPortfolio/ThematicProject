import discord
from discord import app_commands
from discord.ext import commands
import requests
from variablesImport import API_KEY_FOR_MESSAGE_FILTERING

class NaturalLanguage(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    # Define a slash command to ask AI a question
    @app_commands.command(name="ask_ai", description="Ask a question to the AI model")
    async def natural_language(self, interaction: discord.Interaction, question: str): 
        try:

            # URL to API endpoint for bot
            url = "https://chatgpt-ai-chat-bot.p.rapidapi.com/ask"

            # The question being asked
            payload = {"query": question}

            # Headers, including the API key
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": API_KEY_FOR_MESSAGE_FILTERING,
                "X-RapidAPI-Host": "chatgpt-ai-chat-bot.p.rapidapi.com"
            }

            # Get the response to the question
            response = requests.post(url, json=payload, headers=headers)

            # Get the respnse from the JSON data returned
            data = response.json()
            
            # Extract the 'response' parameter from the JSON
            answer = data["response"]

            # Send a message with the response
            await interaction.response.send_message(content=answer, ephemeral=True)
        
        # Include an except block to handle exceptions
        except Exception as e:
            await interaction.response.send_message(content="An error occurred while processing your request.", ephemeral=True)
            print(e)

# Define a setup function to add the cog to the bot 
async def setup(client:commands.Bot) -> None:
    await client.add_cog(NaturalLanguage(client))
