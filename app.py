import discord
from discord.ext import commands

# Define the intents your client will use
intents = discord.Intents.all()
#intents.messages = True  # Enable the ability to receive message events

# Initialize the Client object with the defined intents
bot = commands.Bot(command_prefix='emp!', intents=intents)

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.command(help="Says hello back to whoever said hello")
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')



@bot.command(help="Lists all the bot's commands and what they do")
async def aboutcommands(ctx):
    embed = discord.Embed(
        title="Empowerment Bot Commands List",
        description="Here are all the commands that I can perform:",
        color=discord.Color.red()
    )

    for command in bot.commands:
        embed.add_field(name=f"emp!{command.name}", value=command.help, inline=False)

    await ctx.send(embed=embed)


# Run the bot with your bot token
bot.run()