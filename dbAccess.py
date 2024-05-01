import logging
import os
import json
import pymongo
from variablesImport import MONGODBPATH

#Checks Mongo DB Path
if MONGODBPATH == '':
    logging.error("Mongo DB Path not provided.")
    exit()

database_access_url = str(MONGODBPATH)

database = pymongo.MongoClient(database_access_url)

db = database['BoomBot']

servers = db['servers']

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

print(checkIfCommandIsActive(1210173480344092674, 'DefaultCommands', 'status'))