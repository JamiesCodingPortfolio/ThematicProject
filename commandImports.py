import os
import importlib.util
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

def loadCommands(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.py'):
            module_name = file_name[:-3]  # Remove the .py extension
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(folder_path, file_name))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, commands.Command):
                    bot.add_command(attr)