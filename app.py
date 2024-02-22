import discord
from discord.ext import commands

# Define the intents your client will use
intents = discord.Intents.default()
intents.messages = True  # Enable the ability to receive message events

# Initialize the Client object with the defined intents
bot = commands.Bot(command_prefix='boom!', intents=intents)

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.command()
async def hello(ctx):
    print('Hello command executed')
    await ctx.send('Hello {0.author.mention}!')

bot.run('MTIxMDE1MjE2NzA0NzE3NjI2Mg.GxNgJN.EEDDAXX8XGAxBh5NLE40pTzXoYHhVQI__UDb-0')