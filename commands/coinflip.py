from time import time
import random

from config import COMMAND_PREFIX, USER_RESPAWN_TIME
from utils.users import get_user, load_users, set_user


async def cmd_coinflip(username, reply, args=None):
    print(f"@{username} requested a coin flip command with args: {args}")

    args = args or []

    if len(args) < 2:
        await reply(
            f"@{username} Usage: "
            f"{COMMAND_PREFIX}coinflip <heads | tails> <amount>"
        )
        return

    side = args[0].lower()
    if side not in ("heads", "tails"):
        await reply(
            f"@{username} Choose 'heads' or 'tails' KEKP"
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
        hours = int((user["death_time"] + USER_RESPAWN_TIME - time()) / 3600)
        minutes = int((user["death_time"] + USER_RESPAWN_TIME - time()) % 3600 / 60)
        seconds = int((user["death_time"] + USER_RESPAWN_TIME - time()) % 60)
        
        await reply(f"@{username} You are dead KEKP | You will respawn in {str(hours) + 'h' if hours != 0 else ''} {str(minutes) + 'm' if minutes != 0 else ''} {seconds}s")
        return

    if args[1].lower() == "all":
        amount = user["balance"]
    else:
        try:
            amount = int(args[1])
        except ValueError:
            await reply(
                f"@{username} Enter a valid number KEKP"
            )
            return

    if amount <= 0:
        await reply(
            f"@{username} You cannot bet 0 or a negative amount 🍪 KEKWhat"
        )
        return

    if amount > user["balance"]:
        await reply(
            f"@{username} You don't have enough 🍪 KEKScreen"
        )
        return

    result = random.choice(["heads", "tails"])
    if result == side:
        user["balance"] += amount
        user["coinflip_wins"] += 1
        
        if amount > user["coinflip_biggest_win"]:
            user["coinflip_biggest_win"] = amount
        
        result_text = f"+{amount}"
        emote = "KEKP Clap"
    else:
        user["balance"] -= amount
        user["coinflip_losses"] += 1
        
        if amount > user["coinflip_biggest_loss"]:
            user["coinflip_biggest_loss"] = amount
        
        result_text = f"-{amount}"
        emote = "KEKScreen"

    set_user(username, user)

    await reply(
        f"@{username} Coin lands on {result} {emote} | "
        f"Change: {result_text} 🍪 | "
        f"Balance: {user['balance']} 🍪"
    )