from discord.ext import commands
import requests
from variablesImport import API_KEY_FOR_MESSAGE_FILTERING

class message_filtering(commands.Cog):
    def __init__(self, client: commands.Bot):
        # Initialise the class with the Discord client
        self.client = client

    async def contains_profanity(self, text):
        # Define the URL for the PurgoMalum API request
        url = "https://community-purgomalum.p.rapidapi.com/containsprofanity"

        # Define the headers, which include the API key and host
        headers = {
            "X-RapidAPI-Key": API_KEY_FOR_MESSAGE_FILTERING,
            "X-RapidAPI-Host": "community-purgomalum.p.rapidapi.com"
        }

        # Define the parameter, which is the text of the message we want to check
        params = {"text": text}
        
        # Send a GET request to the PurgoMalum API with the information specified
        response = requests.get(url, headers=headers, params=params)

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Return True if the response body contains the boolean value True, indicating profanity
            return response.json()
        
        # Return False if there was an error in the request or the message doesn't contain profanity
        else:
            return False
        
    # Event listener for message events
    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if the message contains profanity using PurgoMalum API
        if await self.contains_profanity(message.content) == True:

            # If profanity is detected, delete the message
            await message.delete()

            # Send a direct message to the author informing them that their message has been deleted
            await message.author.send("Your message has been deleted because it contains inappropriate content.")
            
# Define a setup function to add the cog to the bot
async def setup(client:commands.Bot) -> None:
    await client.add_cog(message_filtering(client))