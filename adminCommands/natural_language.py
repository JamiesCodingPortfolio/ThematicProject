import discord
from discord import app_commands
from discord.ext import commands
import requests

class NaturalLanguage(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.conversation_context = {}

    @app_commands.command(name="ask_ai", description="Ask a question to the AI model")
    async def natural_language(self, interaction: discord.Interaction, question: str): 
        try:

            url = "https://chatgpt-ai-chat-bot.p.rapidapi.com/ask"

            payload = {"query": question}

            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": "ddd6ad419amsh26df8d7beb422b5p1c9cdejsn5f27cc21c893",
                "X-RapidAPI-Host": "chatgpt-ai-chat-bot.p.rapidapi.com"
            }

            response = requests.post(url, json=payload, headers=headers)

            data = response.json()
            
            answer = data["response"]

            await interaction.response.send_message(content=answer, ephemeral=True)
        
        except Exception as e:
            await interaction.response.send_message(content="An error occurred while processing your request.", ephemeral=True)
            print(e)

# Define a setup function to add the cog to the bot 
async def setup(client:commands.Bot) -> None:
    await client.add_cog(NaturalLanguage(client))
