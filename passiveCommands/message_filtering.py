from discord.ext import commands
import requests
from variablesImport import API_KEY_FOR_MESSAGE_FILTERING
from adminCommands.timeout_with_questionnaire import timeout_with_questionnaire # Import the timeout with questionnaire cog to timeout a user

class message_filtering(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.profanity_count = {}

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

            # Get the user ID
            user_id = str(message.author.id)

            # Increment the profanity count for the user
            self.profanity_count[user_id] = self.profanity_count.get(user_id, 0) + 1

            # Check if the user has reached the profanity limit
            if self.profanity_count[user_id] >= 3:

                # If the limit is reached, timeout the user
                await timeout_with_questionnaire(message.author)  # Call the timeout function from timeout.py

                # Inform the user about the timeout reason
                await message.author.send("You have been timed out for using profanity multiple times. Please refrain from using inappropriate language.")
                
                # Reset the profanity count for the user
                self.profanity_count[user_id] = 0


            else:

                # If the user hasn't reached the limit, inform them about the remaining warnings
                warnings_left = 3 - self.profanity_count[user_id]
                await message.author.send(f"Warning: You have {warnings_left} warnings left before being timed out. Please refrain from using inappropriate language.")

            # If profanity is detected, delete the message
            await message.delete()
    
    
# Define a setup function to add the cog to the bot
async def setup(client:commands.Bot) -> None:
    await client.add_cog(message_filtering(client))