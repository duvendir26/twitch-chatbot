import random

from time import time
from utils.users import load_users, set_user

SUCCESS_RATE = 0.35
FATAL_FAILURE_RATE = 0.05 # Thief loses hp and balance (or even dies) on this chance
MIN_STEAL_BALANCE = 10
STEAL_COOLDOWN = 30 * 60
ACTIVE_TIME_LIMIT = 15 * 60
COOLDOWN_IMMUNITY = ["the_kekbot"] #? FOR TESTING

# Stealing should also hurt target on success (reduce their HP) and on failure thief should lose hp or even lose all (on rare chance) and then he drops his whole balance
# It can also hurt both players
# You cant steal from someone who is dead and also not in chat (track last message time) if its past 15 min
# Honor system (if you steal you lose honor but if you give away you gain it)
# Low honor cant duel

async def cmd_steal(username, reply, args=None):
    print(f"@{username} requested steal command with args: {args}")

    if not args:
        await reply(
            f"@{username} Usage: $steal <target_username>"
        )
        return

    target_username = args[0]
    if target_username.lower() == username.lower():
        await reply(
            f"@{username} You cannot steal from yourself KEKWhat"
        )
        return

    users = load_users()
    user = next(
        (
            user for user in users
            if user["username"].lower() == username.lower()
        ),
        None
    )

    if not user:
        await reply(
            f"@{username} You are not registered. "
            f"Use $kek to register KEKP"
        )
        return
    
    if user["hp"] <= 0:
        hours = int((user["death_time"] + 24 * 60 * 60 - time()) / 3600)
        minutes = int((user["death_time"] + 24 * 60 * 60 - time()) % 3600 / 60)
        seconds = int((user["death_time"] + 24 * 60 * 60 - time()) % 60)
        
        await reply(f"@{username} You are dead KEKP | You will respawn in {str(hours) + 'h' if hours != 0 else ''} {str(minutes) + 'm' if minutes != 0 else ''} {seconds}s")
        return
     
    if user["balance"] < MIN_STEAL_BALANCE:
        await reply(
            f"@{username} You need at least "
            f"{MIN_STEAL_BALANCE} 🍪 to attempt a steal KEKP"
        )
        return

    current_time = int(time())
    steal_timer = user.get("steal_timer", 0)
    if current_time < steal_timer and username.lower() not in COOLDOWN_IMMUNITY:
        remaining = steal_timer - current_time
        minutes = remaining // 60
        seconds = remaining % 60

        await reply(
            f"@{username} You need to wait "
            f"before stealing again KEKP "
            f"| Cooldown: {(str(minutes) + 'm' if minutes > 0 else '')} {seconds}s "
        )
        return

    target_user = next(
        (
            user for user in users
            if user["username"].lower() == target_username.lower()
        ),
        None
    )

    if not target_user:
        await reply(
            f"@{username} User '{target_username}' "
            f"not found (didn't use $kek) KEKP"
        )
        return
    
    if target_user["username"].lower() == "the_kekbot":
        await reply(
            f"@{username} You cannot steal from the bot KEKP"
        )
        return
    
    if target_user["hp"] <= 0:
        hours = int((target_user["death_time"] + 24 * 60 * 60 - time()) / 3600)
        minutes = int((target_user["death_time"] + 24 * 60 * 60 - time()) % 3600 / 60)
        seconds = int((target_user["death_time"] + 24 * 60 * 60 - time()) % 60)
        
        await reply(f"@{username} User '{target_user['username']}' is dead KEKP | Will respawn in {str(hours) + 'h' if hours != 0 else ''} {str(minutes) + 'm' if minutes != 0 else ''} {seconds}s")
        return
    
    if target_user["last_seen"] < int(time.time()) - ACTIVE_TIME_LIMIT:
        await reply(
            f"@{username} User '{target_user['username']}' was not active in the last {ACTIVE_TIME_LIMIT // 60} minutes (last seen {time.strftime('%d.%m.%Y %H:%M:%S', time.localtime(target_user['last_seen']))} CEST) KEKP"
        )
        return

    if target_user["balance"] <= 0:
        await reply(
            f"@{username} @{target_user['username']} has no 🍪 to steal KEKP"
        )
        return

    max_steal = min(
        user["balance"] * 2,
        target_user["balance"]
    )

    amount = random.randint(1, max_steal)

    user["steal_timer"] = current_time + STEAL_COOLDOWN

    success = random.random() < SUCCESS_RATE
    if success:
        target_user["balance"] -= amount
        user["balance"] += amount

        set_user(target_user["username"], target_user)
        set_user(user["username"], user)

        await reply(
            f"@{username} Stole {amount} 🍪 "
            f"from {target_user['username']} KEKP "
        )

    else:
        penalty = amount // 2
        penalty = min(penalty, user["balance"])

        user["balance"] -= penalty

        set_user(user["username"], user)

        await reply(
            f"@{username} Got caught stealing from "
            f"{target_user['username']} and lost -{penalty} 🍪 ALERT creaturePolice ALERT"
        )