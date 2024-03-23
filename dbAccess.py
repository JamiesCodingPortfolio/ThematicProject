#Imports error logging
import logging

#Imports pathing commands
from pathlib import Path

#Imports required pymongo library
import pymongo

#Finds file paths
desktop_path = Path.home() / "Desktop"

database_access = desktop_path / "database_access.txt"

if not database_access.is_file():
    logging.error("Token file not found.")
    exit()

MONGODBPATH = ''

with open("variables.txt", "r") as file:
        # Read the content of the file
    content = file.read()

# Split the content by '=' to separate the variable name and its value
variable_name, value = content.split('=')

# Remove any leading or trailing whitespace from the value
value = value.strip()

# Create the variable dynamically using globals()
globals()[variable_name.strip()] = value

# Test the variable
print(MONGODBPATH)

with open(database_access, 'r') as file:
    database_access_url = file.read()

database = pymongo.MongoClient(database_access_url)

db = database['BoomBot']

servers = db['servers']

result = servers.find()
for document in result:
    print (document["Server ID"])