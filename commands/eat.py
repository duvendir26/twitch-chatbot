# Eating should heal player and reduce bonus cooldown.
# If player has 0 health there is a respawn timer for 24 hours. He comes back with 10hp and then he can use other commands.
# While dead he cant use anything and nobody can use anything on him.
from time import time
from config import COMMAND_PREFIX
from utils.users import load_users


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

    # Implement eating logic here (e.g., heal player, reduce bonus cooldown, etc.)