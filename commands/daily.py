import random

DAILY_MIN = 0
DAILY_MAX = 25

GAIN_CHANCE = 0.8
LOSE_CHANCE = 0.2


async def cmd_daily(username, reply, args=None):
    amount = random.randint(DAILY_MIN, DAILY_MAX)
    if random.random() < GAIN_CHANCE:
        await reply(
            f"@{username} +{amount} 🍪"
        )
    else:
        await reply(
            f"@{username} -{amount} 🍪"
        )