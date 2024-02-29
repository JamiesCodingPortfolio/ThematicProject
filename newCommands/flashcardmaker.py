from app import bot

# Initialize the bot
bot = commands.Bot(command_prefix='!')

# Dictionary to store flashcards
flashcards = {}

# Command to make a flashcard
@bot.command()
async def flashcardmaker(ctx):
    concept = input("Enter the concept: ")
    if concept in flashcards:
        await ctx.send(f"{concept} already exists in the flashcards.")
    else:
        definition = input("Enter the definition: ")
        flashcards[concept] = definition
        await ctx.send(f"Flashcard created for **{concept}** with definition **{definition}**.")

# Command to retrieve a flashcard
@bot.command()
async def flashcarddefinition(ctx, *, concept):
    if concept in flashcards:
        definition = flashcards[concept]
        await ctx.send(f"**{concept}**: {definition}")
    else:
        await ctx.send(f"No flashcard found for **{concept}**.")