import logging
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