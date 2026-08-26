# Loan system for all players
# Ask for loan, accept
# Repay loan
# How to prevent loan abuse (players taking out loans and not repaying them)
# Could implement a system where players have to pay back loans with interest, and if they fail to repay, they could face penalties such as reduced credit score or limited access to future loans. Additionally, there could be a maximum loan limit based on the player's in-game performance or reputation.
# 1 hour time to repay a loan with fixed interest but after that it will increase and player that gave loan can use a command to collect the loan or wait for interest to build up
# Player that loaned has a command to repay the loan 
# There is also a command to see your loans and for people to see how much they are owed 
# so commands loan, repay, collect, loans (shows both your loans and loans owed to you)

from time import time
from utils.users import load_users


async def cmd_loan(username, reply, args=None):
    print(f"@{username} requested loan command with args: {args}")

    users = load_users()
    user = next((u for u in users if u['username'].lower() == username.lower()), None)
    if not user:
        await reply(f"@{username} You are not registered. Use $kek to register KEKP")
        return
    
    if user["hp"] <= 0:
        hours = int((user["death_time"] + 24 * 60 * 60 - time()) / 3600)
        minutes = int((user["death_time"] + 24 * 60 * 60 - time()) % 3600 / 60)
        seconds = int((user["death_time"] + 24 * 60 * 60 - time()) % 60)
        
        await reply(f"@{username} You are dead KEKP | You will respawn in {str(hours) + 'h' if hours != 0 else ''} {str(minutes) + 'm' if minutes != 0 else ''} {seconds}s")
        return