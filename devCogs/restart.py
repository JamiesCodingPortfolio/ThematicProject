#Imports bot to run commands

from app import bot

@bot.command(help="restarts the bot completely")
async def restartbot():
    restart()

    #Currently does not work do not use!
def restart():
    import sys
    print("argv was",sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")

    import os
    os.execv(sys.executable, ['python'] + sys.argv)