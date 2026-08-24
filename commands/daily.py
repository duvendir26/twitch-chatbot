import random

from time import time
from utils.users import get_user, set_user

DAILY_MIN = 1
DAILY_MAX = 30

GAIN_CHANCE = 0.8
LOSE_CHANCE = 0.2

COOLDOWN_TIME = 15 * 60
COOLDOWN_IMMUNITY = ["the_kekbot"] #? FOR TESTING

messagesZero = [
    "You found no keks today. Better luck tomorrow KEKBye",
    "No keks for you today. Try again later KEKBye",
    "You were too busy to collect keks today KEKBye",
]

messagesGain = [
    "You found a hidden stash of keks KEKShook",
    "You inherited some keks from a distant relative KEKP Clap",
    "You were gifted keks by a generous stranger KEKScreen",
]

messagesLose = [
    "You gave your keks to a stranger KEKP Love",
    "You were abducted by aliens and they took your keks AlienPls KEK7",
    "You donated your keks to charity KEKP Love",
]

messagesTime = [
    "You must wait before claiming your next daily reward KEKScreen",
    "You are too early to collect your keks KEKScreen",
    "You have already collected your keks KEKScreen",
]

async def cmd_daily(username, reply, args=None):
    print(f"@{username} requested daily command with args: {args}")
    #!---------------------------------------------------------------------------------------
    
    user = get_user(username)
    last_daily = int(user["last_daily"])
    
    minutes = int((last_daily + COOLDOWN_TIME - time()) / 60)
    seconds = int((last_daily + COOLDOWN_TIME - time()) % 60)
    if username not in COOLDOWN_IMMUNITY and last_daily + COOLDOWN_TIME > time():
        await reply(f"@{username} {random.choice(messagesTime)} | Balance: {user['balance']} 🍪 | Cooldown: {minutes}m {seconds}s")
        return
    
    amount = random.randint(DAILY_MIN, DAILY_MAX)
    roll = random.random()
    
    if roll == 0.05:
        await reply(
            f"@{username} {random.choice(messagesZero)} | +0 🍪"
        )
    elif roll < GAIN_CHANCE and not roll == 0.05:
        await reply(
            f"@{username} {random.choice(messagesGain)} | +{amount} 🍪"
        )
    else:
        await reply(
            f"@{username} {random.choice(messagesLose)} | -{amount} 🍪"
        )
        
    if roll < GAIN_CHANCE:
        user["balance"] += amount
    else:
        user["balance"] -= amount
        
    user["last_daily"] = int(time())
    set_user(username, user)