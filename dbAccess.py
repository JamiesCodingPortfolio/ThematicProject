import logging
import os
import json
import pymongo
from variablesImport import MONGODBPATH
from bot import prfx

#Checks Mongo DB Path
if MONGODBPATH == '':
    logging.error("Mongo DB Path not provided.")
    exit()

database_access_url = str(MONGODBPATH)

database = pymongo.MongoClient(database_access_url)

db = database['BoomBot']

servers = db['testservers']

def dbUpdate(serverID):
    mismatched_servers = []  # Empty list to store server IDs with mismatches
    with open('JsonExample.json', 'r') as json_file:
        json_data = json.load(json_file)
            
    server_id = str(serverID)
    existing_document = servers.find_one({'ServerID': server_id})
            
    if 'DefaultCommands' in existing_document and 'DefaultCommands' in json_data:
        if existing_document['DefaultCommands'] != json_data['DefaultCommands']:
            mismatched_servers.append(server_id)  # Add server ID to list

    if mismatched_servers:  # Check if there are mismatches
        return "Documents for the following servers do not match JsonExample:\n" + ", ".join(mismatched_servers) + "\nConsider updating the documents or JsonExample."
    else:
        return "JSON Data matches what is currently within Database when compared to JsonExample."

def checkIfCommandIsActive(serverID, commandGroup, commandName):
    server_id = str(serverID)
    
    existing_document = servers.find_one({'ServerID': server_id})
    
    if commandGroup in existing_document:
        
        if commandName in existing_document[commandGroup]:
            
            return existing_document[commandGroup][commandName]['active']

        return False
    
    print("Command Group does not exist.")

def createServerInDatabase(serverID):
    server_id = str(serverID)
    
    admin_commands_dir = os.path.join(os.path.dirname(__file__), 'adminCommands')
    commands_dir = os.path.join(os.path.dirname(__file__), 'Commands')
    
    admin_commands_files = [f for f in os.listdir(admin_commands_dir) if f.endswith('.py')]
    commands_files = [f for f in os.listdir(commands_dir) if f.endswith('.py')]
    
    def create_commands_dict(files):
        return {file[:-3]: {'active': False} for file in files}
    
    admin_commands_dict = create_commands_dict(admin_commands_files)
    commands_dict = create_commands_dict(commands_files)
    
    existing_document = db["servers"].find_one({'ServerID': server_id})
    
    if existing_document is None:
        new_document = {
            "ServerID": server_id,
            "adminCommands": admin_commands_dict,
            "Commands": commands_dict,
        }
        db["servers"].insert_one(new_document)
        print(f"Created JSON document for server: {server_id}")
        
    else:
        # If a document already exists, update the categories as needed
        updated = False

        # Update adminCommands if necessary
        if 'adminCommands' not in existing_document:
            existing_document['adminCommands'] = admin_commands_dict
            updated = True

        # Update Commands if necessary
        if 'Commands' not in existing_document:
            existing_document['Commands'] = commands_dict
            updated = True

        # If there were updates to the existing document, save the changes
        if updated:
            db["servers"].update_one({'ServerID': server_id}, {'$set': existing_document})
            print(f"Updated document for server: {server_id}")
            