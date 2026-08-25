# Every month, the bot will reset the stats for all users
# We need season command to check how long until the next season reset

from datetime import date
from time import time


async def cmd_season(username, reply, args=None):
    print(f"@{username} requested season command with args: {args}")
  
    #!TODO: finish this