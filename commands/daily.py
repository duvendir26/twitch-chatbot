import random

DAILY_MIN = 0
DAILY_MAX = 25

GAIN_CHANCE = 0.8
LOSE_CHANCE = 0.2

COOLDOWN_IMMUNITY = ["the_kekbot"]

messagesZero = [
    "You found no keks today. Better luck tomorrow KEKBye",
    "No keks for you today. Try again later KEKBye",
    "You were too busy to collect keks today KEKBye",
]

messagesGain = [
    "You found a hidden stash of keks KEKShook",
    "You won a kek lottery KEKP Clap",
    "You were gifted keks by a generous stranger KEKScreen",
]

messagesLose = [
    "You gave your keks to a stranger KEKP Love",
    "You were abducted by aliens and they took your keks AlienPls KEKP",
    "You donated your keks to charity KEKP Love",
]


async def cmd_daily(username, reply, args=None):
    amount = random.randint(DAILY_MIN, DAILY_MAX)
    roll = random.random()
    
    if roll == 0.05:
        await reply(
            f"@{username} {random.choice(messagesZero)} | +0 🍪"
        )
    elif roll < GAIN_CHANCE:
        await reply(
            f"@{username} {random.choice(messagesGain)} | +{amount} 🍪"
        )
    else:
        await reply(
            f"@{username} {random.choice(messagesLose)} | -{amount} 🍪"
        )