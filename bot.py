import os
import json
import discord
import itertools
from discord.ext import commands
from colorama import Back, Fore, Style
import time
import platform
import socket
from variablesImport import ADMINCHANNEL

prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)

import dbAccess

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=discord.Intents().all())
        self.devCogs = ["setupCogs.dbchecks"]
        self.cogslist = ["Commands.hello","Commands.status","adminCommands.remove_messages","passiveCommands.message_filtering", "passiveCommands.response_to_messages", "adminCommands.soft_ban", "adminCommands.natural_language","adminCommands.timeout", "adminCommands.timeout_with_questionnaire"]
        self.db = dbAccess.db
        self.servers = dbAccess.servers
        
        
        
    async def setup_hook(self):
        for ext in self.devCogs:
            await self.load_extension(ext)
        for ext in self.cogslist:
            await self.load_extension(ext)
        
    async def on_ready(self):
        print (prfx + " Logged in as " + Fore.YELLOW + self.user.name)
        print (prfx + " Bot ID " + Fore.YELLOW + str(self.user.id))
        print (prfx + " Discord Version " + Fore.YELLOW + str(platform.python_version()))
        print (prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        
        for guild in self.guilds:
            server_id = str(guild.id)
            
            dbAccess.createServerInDatabase(server_id)
            
        print("All servers have been checked and updated")
            
        
        synced = await self.tree.sync()
        for item in synced:
            if item:
                print(prfx + " Imported: " + Fore.YELLOW + str(item))
            else:
                print(prfx + " Failed to import commands from: " + Fore.RED + str(item))
        print (prfx + " Slash CMDs Synced " + Fore.YELLOW + str(len(synced)) + " Commands")
        
        print('Logged in as {0.user}'.format(self))
        adminChannel = self.get_channel(int(ADMINCHANNEL))
        if adminChannel is not None:
            await adminChannel.send('The bot is running and the PC currently running this bot is ' + socket.gethostname())
        else:
            print("Channel not found.")
            