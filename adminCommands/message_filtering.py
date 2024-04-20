from discord.ext import commands
import requests

class message_filtering(commands.Cog):
    def __init__(self, client: commands.Bot):
        # Initialize the class with the Discord client
        self.client = client
        # Initialize the profanity check object

    async def contains_profanity(self, text):
        # Define the URL for the PurgoMalum API request
        url = "https://community-purgomalum.p.rapidapi.com/containsprofanity"

        # Define the headers, which include the API key and host
        headers = {
            "X-RapidAPI-Key": "ddd6ad419amsh26df8d7beb422b5p1c9cdejsn5f27cc21c893",
            "X-RapidAPI-Host": "community-purgomalum.p.rapidapi.com"
        }

        # Define the parameters, which is the text of the message we want to check
        params = {"text": text}
        
        # Send a GET request to the PurgoMalum API with the information specified
        response = await requests.get(url, headers=headers, params=params)

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Return True if the response body contains the boolean value True, indicating profanity
            return response.json() == True
        
        # Return False if there was an error in the request or the message doesn't contain profanity
        else:
            return False
        
    # Event listener for message events
    async def on_message(self, message):
        # Check if the message contains profanity using PurgoMalum API
        if await self.contains_profanity(message.content):

            # If profanity is detected, delete the message
            await message.delete()

            # Send a direct message to the author informing them that their message has been deleted
            await message.author.send("Your message has been deleted because it contains inappropriate content.")
            

async def setup(client:commands.Bot) -> None:
    await client.add_cog(message_filtering(client))