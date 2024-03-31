#Imports error logging
import logging

#Imports pathing commands
from pathlib import Path

#Imports required pymongo library
import pymongo

#import the database path
from variablesImport import MONGODBPATH

#Finds file paths
desktop_path = Path.home() / "Desktop"

database_access = desktop_path / "database_access.txt"

if not database_access.is_file():
    logging.error("Token file not found.")
    exit()

database_access_url = str(MONGODBPATH)

database = pymongo.MongoClient(database_access_url)

db = database['BoomBot']

servers = db['servers']

result = servers.find()
for document in result:
    print (document["Server ID"])