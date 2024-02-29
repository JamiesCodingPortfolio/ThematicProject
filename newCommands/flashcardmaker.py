from discord.ext import commands
import asyncio

# Dictionary to store flashcards
userflashcards = {}

# Command to make a flashcard
@commands.command()
async def makeflashcard(ctx):
    user_id = str(ctx.author.id)

    if user_id not in userflashcards:
        userflashcards[user_id] = {}

    await ctx.send("Enter the concept: ")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        concept_msg = await ctx.bot.wait_for("message", check=check, timeout=30)
        concept = concept_msg.content

        if concept in userflashcards[user_id]:
            await ctx.send(f"{concept} already exists in your flashcards.")
        else:
            await ctx.send("Enter the definition: ")
            definition_message = await ctx.bot.wait_for("message", check=check, timeout=30)
            definition = definition_message.content
            userflashcards[user_id][concept] = definition
            await ctx.send(f"Flashcard created for **{concept}** with definition **{definition}**.")

    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Command canceled.")

# Command to retrieve a flashcard
@commands.command()
async def defineflashcard(ctx, *, concept=None):
    user_id = str(ctx.author.id)
    
    # Check if concept is missing
    if concept is None:
        await ctx.send("Please provide a concept to define.")
        return

    if user_id in userflashcards and concept in userflashcards[user_id]:
        definition = userflashcards[user_id][concept]
        await ctx.send(f"**{concept}**: {definition}")
    else:
        await ctx.send(f"No flashcard found for **{concept}**.")