from discord.ext import commands
import asyncio

# Dictionary to store flashcards
userflashcards = {}

# Command to make a flashcard
@commands.command(help="Creates a new flashcard with a concept and definition")
async def makeflashcard(ctx):

    # Get the user ID
    user_id = str(ctx.author.id)

    # Check if user ID exists in the flashcards dictionary
    if user_id not in userflashcards:
        userflashcards[user_id] = {}

    # Prompt user to enter the concept
    await ctx.send("Enter the concept: ")

    # Define a check function to validate messages (check if the message is sent by the same user and in the same channel as the command)
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        # Wait for the user to enter the concept message
        concept_msg = await ctx.bot.wait_for("message", check=check, timeout=30)
        concept = concept_msg.content

        # Check if concept already exists in user's flashcards
        if concept in userflashcards[user_id]:
            await ctx.send(f"{concept} already exists in your flashcards.")
        else:
            # Prompt user to enter the definition
            await ctx.send("Enter the definition: ")

            # Wait for the user to enter the definition message
            definition_message = await ctx.bot.wait_for("message", check=check, timeout=30)
            definition = definition_message.content

            # Add the flashcard to the user's dictionary
            userflashcards[user_id][concept] = definition
            await ctx.send(f"Flashcard created for **{concept}** with definition **{definition}**.")

    # Cancel command if user takes too long to enter a concept
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Command cancelled.")


# Command to retrieve a flashcard
@commands.command(help="Gives the definition of an existing flash card concept")
async def defineflashcard(ctx, *, concept=None):

    # Get the user ID
    user_id = str(ctx.author.id)
    
    # Check if concept is missing
    if concept is None:
        await ctx.send("Please provide a concept to define.")
        return

    # Check if user ID exists in the flashcards dictionary and concept exists for the user
    if user_id in userflashcards and concept in userflashcards[user_id]:
        definition = userflashcards[user_id][concept]
        await ctx.send(f"**{concept}**: {definition}")
    else:
        await ctx.send(f"No flashcard found for **{concept}**.")


# Command to delete a flashcard
@commands.command( help="Deletes a flash card if it exists")
async def deleteflashcard(ctx, *, concept=None):

    # Get the user ID
    user_id = str(ctx.author.id)
    
    # Check if concept is missing
    if concept is None:
        await ctx.send("Please provide a concept to delete.")
        return

    # Check if user ID exists in the flashcards dictionary and concept exists for the user
    if user_id in userflashcards and concept in userflashcards[user_id]:
        del userflashcards[user_id][concept]
        await ctx.send(f"Flashcard for **{concept}** deleted successfully.")
    else:
        await ctx.send(f"No flashcard found for **{concept}**.")