import discord

# Define the intents your bot will use
intents = discord.Intents.default()
intents.messages = True  # Enable the ability to receive message events

# Initialize the Bot object with the defined intents and command prefix
bot = commands.Bot(command_prefix='boom!', intents=intents)

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.command()
async def hello(ctx):
    print('Hello command executed')
    await ctx.send('Hello {0.author.mention}!')