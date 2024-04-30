import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from fuzzywuzzy import fuzz  # Import fuzz from fuzzywuzzy for partial string matching

class timeout_with_questionnaire(commands.Cog):
    def __init__(self, client):
        self.client = client  # Assign the bot instance to a class attribute
        self.timeout_room = {}  # Initialize a dictionary to store users in timeout
        self.original_channel_permissions = {}  # Initialize a dictionary to store original channel permissions

        # Define a list of dictionaries for the server rules survey questions and answers
        self.rules_survey = [
            {"question": "What is NSFW and who isn't allowed to see it?", "answer": "NSFW stands for 'Not Safe For Work', and it is content that is not suitable for viewing by minors or individuals in professional or public settings."},
            {"question": "Why is harassment and cyberbullying forbidden?", "answer": "Harassment and cyberbullying are forbidden to ensure a safe and inclusive environment for all members of the community."},
            {"question": "Messaging is fine, but what action should you not do when sending messages?", "answer": "Spamming"},
            {"question": "In which channel is posting your own videos only allowed?", "answer": "Self-promotion"},
        ]

    @app_commands.command(name="timeout_user", description="Puts a user in timeout, where they must answer questions about the server rules or be set free manually")
    async def timeout(self, ctx, user: discord.Member):  # Define a slash command to put a user in timeout
        if user == ctx.author:  # Check if the user is trying to timeout themselves
            await ctx.send("You can't timeout yourself!")  # Send a message indicating the error
            return

        if user in self.timeout_room:  # Check if the user is already in timeout
            await ctx.send(f"{user.mention} is already in timeout!")  # Send a message indicating the error
            return

        self.original_channel_permissions[user] = {}  # Initialize a dictionary to store original channel permissions for the user
        for channel in ctx.guild.channels:  # Loop through all channels in the guild
            self.original_channel_permissions[user][channel] = channel.overwrites_for(user)  # Store original channel permissions for the user

        try:
            # Create a timeout channel for the user
            timeout_channel = await ctx.guild.create_text_channel(f"timeout-{user.display_name}")
            self.timeout_room[user] = timeout_channel  # Add the user to the timeout room dictionary

            await timeout_channel.set_permissions(user, read_messages=True, send_messages=True)  # Set permissions for the user to read and send messages in the timeout channel

            for channel in ctx.guild.channels:  # Loop through all channels in the guild
                if channel != timeout_channel:  # Exclude the timeout channel and the rules channel
                    await channel.set_permissions(user, read_messages=False)  # Restrict the user from reading messages in other channels

            # Send a message to the user indicating they are in timeout
            await timeout_channel.send(f"{user.mention}, you have been placed in timeout. Please complete the following survey about the server rules.")

            # Ask the user the survey questions
            await self.ask_questions(user, timeout_channel)

        except Exception as e:  # Catch any exceptions that may occur during timeout
            await ctx.send(f"An error occurred: {e}")  # Send an error message

    async def ask_questions(self, user, timeout_channel):  # Define a method to ask the survey questions
        while True:  # Run the loop until all questions are answered correctly or the user is freed
            total_attempts = 3  # Initialize the number of attempts allowed for each question
            current_question = 0  # Initialize the index of the current question
            attempts_left = total_attempts  # Initialize the attempts left for the current set of questions

            while current_question < len(self.rules_survey) and attempts_left > 0:  # Loop through each question in the survey
                question_data = self.rules_survey[current_question]  # Get the current question and answer data
                question = question_data["question"]  # Extract the question text
                await timeout_channel.send(question)  # Send the question to the timeout channel

                def check(message):  # Define a check function for message validation
                    return message.author == user and message.channel == timeout_channel  # Check if the message is from the user and in the timeout channel

                # Wait for the user's response
                response = await self.client.wait_for('message', check=check)

                # Check if the response matches the answer with partial fuzzy string matching of 30 or more
                if fuzz.partial_ratio(response.content.lower(), question_data["answer"].lower()) >= 30:
                    current_question += 1  # Move to the next question if the answer is correct
                else:
                    attempts_left -= 1  # Decrease the number of attempts left if answer is wrong
                    if attempts_left == 0:  # If the user exhausts all attempts
                        await timeout_channel.send("You've used all your attempts. Timeout extended by 5 minutes.")
                        await asyncio.sleep(300)  # Extend timeout by 5 minutes
                        await timeout_channel.send("Please try again.")
                        await asyncio.sleep(30)  # Wait for 30 seconds before allowing the user to try again
                        attempts_left = total_attempts  # Reset attempts left to total attempts for the next set of questions
                    else:
                        await timeout_channel.send(f"That's not the correct answer. You have {attempts_left} attempts left.")  # Send a message indicating incorrect answer

            if current_question == len(self.rules_survey):
                await timeout_channel.send("Congratulations! You've answered all questions correctly. You're now free from timeout.")  # Send a message indicating successful completion of the survey
                await self.remove_timeout(user)  # Remove the user from timeout

    @app_commands.command(name="free_user", description="Manually free a user from timeout")
    @commands.has_permissions(manage_roles=True)
    async def free(self, ctx, user: discord.Member):  # Define a slash command to manually free a user from timeout
        if user in self.timeout_room:  # Check if the user is in timeout
            await self.timeout_room[user].delete()  # Delete the timeout channel
            del self.timeout_room[user]  # Remove the user from the timeout room dictionary
            await self.restore_channel_permissions(user)  # Restore original channel permissions for the user
            await ctx.send(f"{user.mention} has been freed from timeout.")  # Send a message indicating successful removal from timeout
        else:
            await ctx.send(f"{user.mention} is not currently in timeout.")  # Send a message indicating the user is not in timeout

    async def remove_timeout(self, user):  # Define a method to remove the user from timeout
        if user in self.timeout_room:  # Check if the user is in timeout
            await self.timeout_room[user].delete()  # Delete the timeout channel
            del self.timeout_room[user]  # Remove the user from the timeout room dictionary
            await self.restore_channel_permissions(user)  # Restore original channel permissions for the user

    async def restore_channel_permissions(self, user):  # Define a method to restore channel permissions for the user
        for channel, perms in self.original_channel_permissions[user].items():  # Loop through the original channel permissions
            await channel.set_permissions(user, overwrite=perms)  # Restore permissions for each channel

# Define a setup function to add the cog to the bot 
async def setup(client: commands.Bot) -> None:
    await client.add_cog(timeout_with_questionnaire(client))
