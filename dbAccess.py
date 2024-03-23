#Imports pathing commands
from pathlib import Path

#Imports required pymongo library
import pymongo

#Finds file paths
desktop_path = Path.home() / "Desktop"

database_access = desktop_path / "database_access.txt"

with open(database_access, 'r') as file:
    database_access_url = file.read()

database = pymongo.MongoClient(database_access_url)

db = database['BoomBot']

servers = db['servers']

result = servers.find()
for document in result:
    print (document["Server ID"])