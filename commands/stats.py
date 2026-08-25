import time

from utils.users import get_user
from commands.bonus import COOLDOWN_TIME
from config import COMMAND_PREFIX       

#TODO: Players can spend keks to upgrade their stats (hp, armor, strength) and these upgrades will be permanent. Players can also spend keks to reset their stats back to the default values. Players can also spend keks to reset their duel wins and losses back to 0. Players can also spend keks to reset their coinflip wins and losses back to 0. Players can also spend keks to reset their stock portfolio back to the default values. Players can also spend keks to reset their bonus timer back to 0. Players can also spend keks to reset their total claimed back to 0.

async def cmd_stats(username, reply, args=None):
    print(f"@{username} requested stats command with args: {args}")

    user = get_user(username)

    # biggest_win = (
    # f"🪙 Biggest coinflip win: {user['coinflip_biggest_win']} 🍪 | "
    # if user['coinflip_biggest_win'] != 0 else ""
    # )

    # biggest_loss = (
    #     f"🪙 Biggest coinflip loss: {user['coinflip_biggest_loss']} 🍪 | "
    #     if user['coinflip_biggest_loss'] != 0 else ""
    # )
    
    remaining = user["bonus_timer"] + COOLDOWN_TIME - time.time()
    if remaining > 0:
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        bonus_timer = f"Bonus cooldown: {str(minutes) + 'm' if minutes != 0 else ''} {seconds}s"
    else:
        bonus_timer = f"Bonus not claimed ({COMMAND_PREFIX}kek)"

    stats_message = (
        f"@{username} [ "
        f"❤️ {user['hp']} | "
        f"🛡️ {user['armor']} | "
        f"⚡ {user['energy']} | "
        f"⚔️ Wins: {user['duel_wins']} | "
        f"⚔️ Losses: {user['duel_losses']} ] - [ "
        f"Balance: {user['balance']} 🍪 | "
        # f"{biggest_win}"
        # f"{biggest_loss}"
        f"🪙 Winrate: {user['coinflip_wins'] / (user['coinflip_wins'] + user['coinflip_losses']) * 100 if (user['coinflip_wins'] + user['coinflip_losses']) > 0 else 0:.2f}% ] - ["
        f"📉 Stocks: ({', '.join([f'{item['name']}: {item['amount']}' for item in user['portfolio']])}) ] "
        f"- [ {bonus_timer} | "
        f"Total claimed: {user['total_claimed']} 🍪 ]"
    )

    await reply(stats_message)