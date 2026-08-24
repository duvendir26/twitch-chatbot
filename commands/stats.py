import time

from utils.users import get_user
from commands.daily import COOLDOWN_TIME

async def cmd_stats(username, reply, args=None):
    print(f"@{username} requested stats command with args: {args}")

    user = get_user(username)

    biggest_win = (
    f"Biggest Coinflip Win: {user['coinflip_biggest_win']} 🍪 | "
    if user['coinflip_biggest_win'] != 0 else ""
)

    biggest_loss = (
        f"Biggest Coinflip Loss: {user['coinflip_biggest_loss']} 🍪 | "
        if user['coinflip_biggest_loss'] != 0 else ""
    )
    
    remaining = user["last_daily"] + COOLDOWN_TIME - time.time()
    if remaining > 0:
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        last_daily = f"Daily Cooldown: {minutes}m {seconds}s"
    else:
        last_daily = "Daily not claimed ($kek)"

    stats_message = (
        f"@{username} Stats: "
        f"HP: {user['hp']} | "
        f"Armor: {user['armor']} | "
        f"Strength: {user['strength']} | "
        f"Balance: {user['balance']} 🍪 | "
        f"Coinflip Wins: {user['coinflip_wins']} | "
        f"Coinflip Losses: {user['coinflip_losses']} | "
        f"{biggest_win}"
        f"{biggest_loss}"
        f"Win Rate: {user['coinflip_wins'] / (user['coinflip_wins'] + user['coinflip_losses']) * 100 if (user['coinflip_wins'] + user['coinflip_losses']) > 0 else 0:.2f}% | "
        f"{last_daily}"
    )

    await reply(stats_message)