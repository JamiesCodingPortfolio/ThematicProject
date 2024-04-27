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
import dbAccess

prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=discord.Intents().all())
        self.devCogs = ["setupCogs.dbchecks"]
        self.cogslist = ["Commands.hello","Commands.status","adminCommands.remove_messages","adminCommands.message_filtering", "adminCommands.soft_ban", "adminCommands.natural_language","adminCommands.timeout", "adminCommands.timeout_with_questionnaire"]
        self.db = dbAccess.db
        self.servers = dbAccess.servers
        
        
        
    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension(ext)
        for ext in self.devCogs:
            await self.load_extension(ext)
        #self.add_command(flashcardmaker.makeflashcard)
        #self.add_command(flashcardmaker.defineflashcard)
        #self.add_command(flashcardmaker.deleteflashcard)
        
    async def check_servers_against_database(self):
        json_example_path = os.path.join(os.path.dirname(__file__), 'JsonExample.json')
        with open(json_example_path, 'r') as json_file:
            json_data = json.load(json_file)
            
        for guild in self.guilds:
            server_id = str(guild.id)
            existing_document = self.db["servers"].find_one({'ServerID': server_id})
            
            if existing_document is None: #Checks if a document exists within the database with the ID of the server being checked
                
                new_document = json_data.copy() #Uses copy so that it does not override other documents
                new_document['ServerID'] = server_id
                self.db["servers"].insert_one(new_document)
                print(prfx + f" Create JSON file for server: {server_id} ")
            else: #Called if server already exists in database
                if 'DefaultCommands' in existing_document and 'DefaultCommands' in json_data:
                    if existing_document['DefaultCommands'] != json_data['DefaultCommands']:
                        print(prfx + f" Document for server: {server_id} does not match JsonExample. Consider updating the document or JsonExample.")
    
    async def on_ready(self):
        print (prfx + " Logged in as " + Fore.YELLOW + self.user.name)
        print (prfx + " Bot ID " + Fore.YELLOW + str(self.user.id))
        print (prfx + " Discord Version " + Fore.YELLOW + str(platform.python_version()))
        print (prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        await self.check_servers_against_database()
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
            