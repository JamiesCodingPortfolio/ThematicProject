# DiscordBot
Uses the discordpy library.

### Dependencies
https://discordpy.readthedocs.io/en/stable/

https://www.mongodb.com/docs/manual/

### Running the bot on your local system
Found in variables.txt file:
- `MONGODBPATH` by default uses the localhost connection string - change if you're using anything more than the default connection string
- `BOT_TOKEN` make sure to add your personal bot token
- `ADMINCHANNEL` this is for debugging to test the bot is working, put a channelID in here that you want the bot to post in
- `ADMINSERVER` this is so that commands to control the bot such as status and sync will only be present with the server specified