from time import time
from utils.users import load_users, set_user

HEAL_PRICE = 50
HEAL_AMOUNT = 20

async def cmd_eat(username, reply, args=None):
    print(f"@{username} requested eat command with args: {args}")

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

    if user['balance'] < HEAL_PRICE:
        await reply(f"@{username} You don't have enough 🍪 to heal. You need {HEAL_PRICE} 🍪 KEKP")
        return
    
    if user["hp"] >= 100:
        await reply(f"@{username} You are already at full health KEKP")
        return

    amount = min(HEAL_AMOUNT, 100 - user["hp"])
    user["hp"] += amount
    user['balance'] -= HEAL_PRICE
    
    set_user(user["username"], user)
    
    await reply(f"@{username} You can eat them YouCanEatThem | Change: -{HEAL_PRICE} 🍪, +{HEAL_AMOUNT} ❤️ | Current HP: ❤️ {user['hp']}")
