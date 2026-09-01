import random

from config import COMMAND_PREFIX
from utils.users import find_user, load_users, reply_if_dead, reply_if_not_registered, set_user
from utils.amounts import parse_positive_amount


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
    user = find_user(users, username)

    if await reply_if_not_registered(reply, username, user):
        return
    
    if await reply_if_dead(reply, username, user, is_self=True):
        return

    amount = await parse_positive_amount(
        reply,
        username,
        args[1],
        allow_all=True,
        all_amount=user["balance"],
        invalid_message=f"@{username} Enter a valid number KEKP",
        zero_message=f"@{username} You cannot bet 0 or a negative amount 🍪 KEKWhat",
    )
    if amount is None:
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