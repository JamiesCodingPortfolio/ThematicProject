from discord.ext import commands
import discord
import requests
import asyncio
from fuzzywuzzy import fuzz

class message_filtering(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.API_KEY_FOR_MESSAGE_FILTERING = "ddd6ad419amsh26df8d7beb422b5p1c9cdejsn5f27cc21c893"

        self.bad_words_count = {}
        self.questions = {
            "What is NSFW and who isn't allowed to see it?": "NSFW stands for 'Not Safe For Work', and it is content that is not suitable for viewing by minors or individuals in professional or public settings.",
            "Why is harassment and cyberbullying forbidden?": "Harassment and cyberbullying are forbidden to ensure a safe and inclusive environment for all members of the community.",
            "Messaging is fine, but what action should you not do when sending messages?": "Spamming",
            "In which channel is posting your own videos only allowed?": "Self-promotion",
        }

    # Function to check if a message contains profanity using PurgoMalum API
    async def contains_profanity(self, text):
        # Define the URL for the PurgoMalum API request
        url = "https://community-purgomalum.p.rapidapi.com/json"  # Set API URL

        # Define the headers, which include the API key and host
        headers = {
            "X-RapidAPI-Key": self.API_KEY_FOR_MESSAGE_FILTERING,  # Set API key
            "X-RapidAPI-Host": "community-purgomalum.p.rapidapi.com"  # Set API host
        }

        # Define the parameter, which is the text of the message we want to check
        params = {"text": text}  # Set request parameters
        
        # Send a GET request to the PurgoMalum API with the information specified
        response = requests.get(url, headers=headers, params=params)  # Send API request

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Return True if the response body contains the boolean value True, indicating profanity
            return response.json()  # Return API response
        
        # Return False if there was an error in the request or the message doesn't contain profanity
        else:
            return False  # Return False if error occurs
        



    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if the message author is the bot itself
        if message.author == self.client.user:
            return
        
        user_id = message.author.id

        # Check if the message contains profanity
        if await self.contains_profanity(message.content):
            if user_id in self.bad_words_count:
                self.bad_words_count[user_id] += 1
            else:
                self.bad_words_count[user_id] = 1

            remaining_chances = 3 - self.bad_words_count.get(user_id, 0)
            if remaining_chances == 0:
                # If all chances are used, put user in timeout
                await message.delete()  # Delete message
                await self.put_in_timeout(message.author, message.channel)  # Put user in timeout
                self.bad_words_count[user_id] = 0  # Reset bad word count for the user
            else:
                # Inform user about remaining chances
                await message.delete()  # Delete message
                await message.author.send(f"You have {remaining_chances} chances left before you are put in timeout.")  # Notify user

            await message.author.send("Please refrain from using profanity in the server.")  # Notify user
        
        else:
            # Process commands
            await self.client.process_commands(message)  # Process user commands








    # Function to put a user in timeout
    async def put_in_timeout(self, user, channel):
        # Notify the user and create a timeout channel
        await channel.send(f"{user.mention} has been put in timeout.")  # Notify user
        await user.send("You have been put in timeout.")  # Notify user via DM

        # Create a new channel for the user
        timeout_channel_name = f'timeout-{user.name}'  # Generate timeout channel name
        overwrites = {
            channel.guild.default_role: discord.PermissionOverwrite(read_messages=False),  # Set permissions for default role
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True)  # Set permissions for user
        }
        timeout_channel = await channel.guild.create_text_channel(name=timeout_channel_name, overwrites=overwrites)  # Create timeout channel
        await timeout_channel.send(f"{user.mention}, welcome to your timeout channel. Please answer the following questions correctly to be set free. You get 3 chances. If you use all your chances, you have to wait 1 minute before retrying.")  # Notify user in timeout channel

        # Disable user's access to other channels
        for guild_channel in channel.guild.channels:
            if guild_channel != timeout_channel:
                await guild_channel.set_permissions(user, read_messages=False, send_messages=False)  # Disable user's access to other channels

        # Ask questions about server rules
        await self.ask_questions(user, timeout_channel)  # Call function to ask questions






    # Function to ask questions during timeout
    async def ask_questions(self, user, timeout_channel, original_question_index=0):
        total_chances = 3  # Set total chances
        remaining_chances = total_chances  # Initialize remaining chances
        current_question_index = original_question_index  # Initialize current question index

        questions_list = list(self.questions.items())  # Convert questions dictionary to list of tuples

        while current_question_index < len(questions_list):
            question, answer = questions_list[current_question_index]  # Get current question and answer
            while remaining_chances > 0:
                # Ask a question
                await timeout_channel.send(question)  # Send question
                # Wait for user response
                response = await self.bot.wait_for('message', check=lambda m: m.author == user and m.channel == timeout_channel)  # Wait for user response
                # Calculate similarity between response and answer
                ratio = fuzz.ratio(response.content.lower(), answer.lower())  # Calculate similarity using fuzzy string matching
                if ratio >= 50:
                    if current_question_index == len(questions_list) - 1:
                        # If it's the last question and the answer is correct, free the user
                        await timeout_channel.send("Correct!")  # Notify user
                        await asyncio.sleep(1)  # Wait a second before sending the final message
                        await timeout_channel.send("Congratulations! You answered all questions correctly. You are now free from timeout.")  # Notify user
                        await asyncio.sleep(1)  # Wait a second before deleting the timeout channel
                        await timeout_channel.delete()  # Delete timeout channel
                        # Restore user's access to other channels
                        for guild_channel in timeout_channel.guild.channels:
                            await guild_channel.set_permissions(user, read_messages=True, send_messages=True)  # Restore user's access
                        return
                    else:
                        # If the answer is correct, move to the next question
                        await timeout_channel.send("Correct! Next question!")  # Notify user
                        current_question_index += 1  # Move to the next question
                        break
                else:
                    remaining_chances -= 1  # Decrease remaining chances
                    if remaining_chances > 0:
                        await timeout_channel.send(f"Incorrect! Please try again. You have {remaining_chances} chances left.")  # Notify user
                    else:
                        # If all chances are used, extend timeout by 1 minute
                        await timeout_channel.send("Incorrect! You have used all your chances. Timeout extended by 1 minute.")  # Notify user
                        await asyncio.sleep(60)  # Wait for 1 minute
                        remaining_chances = total_chances  # Reset remaining chances
                        current_question_index = original_question_index  # Reset to first question
                        await timeout_channel.send(f"{user.mention} Let's start over. First question!")  # Notify user
                        break



async def setup(bot):
    await bot.add_cog(message_filtering(bot))
