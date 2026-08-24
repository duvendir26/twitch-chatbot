import random

from config import COMMAND_PREFIX
from utils.users import get_user, set_user


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

    user = get_user(username)
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
        result_text = f"+{amount}"
        emote = "KEKP Clap"
    else:
        user["balance"] -= amount
        result_text = f"-{amount}"
        emote = "KEKScreen"

    set_user(username, user)

    await reply(
        f"@{username} Coin lands on {result} {emote} | "
        f"{result_text} 🍪 | "
        f"Balance: {user['balance']} 🍪"
    )