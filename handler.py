from time import time

from commands.bonus import cmd_bonus
from commands.coinflip import cmd_coinflip
from commands.leaderboard import cmd_leaderboard
from commands.bottom import cmd_bottom
from commands.stats import cmd_stats
from commands.commandList import cmd_command_list
from commands.send import cmd_send
from commands.steal import cmd_steal
from commands.stocks import cmd_stocks, cmd_portfolio, cmd_buy, cmd_sell
from commands.eat import cmd_eat

from config import COMMAND_PREFIX
from utils.users import update_last_seen

COMMANDS = {
    "kek": cmd_bonus,
    "bonus": cmd_bonus, #? ALIAS
    # -----------------------------
    "coinflip": cmd_coinflip,
    # -----------------------------
    "leaderboard": cmd_leaderboard,
    "top": cmd_leaderboard, #? ALIAS
    "kekkers": cmd_leaderboard, #? ALIAS
    # -----------------------------
    "stats": cmd_stats,
    "keks": cmd_stats, #? ALIAS
    # ----------------------------
    "bottom": cmd_bottom,
    # ----------------------------
    "commands": cmd_command_list,
    # ----------------------------
    "send": cmd_send,
    "sendkeks": cmd_send, #? ALIAS
    "give": cmd_send, #? ALIAS
    "givekeks": cmd_send, #? ALIAS
    # ----------------------------
    "stocks": cmd_stocks,
    "price": cmd_stocks, #? ALIAS
    "prices": cmd_stocks, #? ALIAS
    # ----------------------------
    "portfolio": cmd_portfolio,
    # ----------------------------
    "buy": cmd_buy,
    # ----------------------------
    "sell": cmd_sell,
    # ----------------------------
    "steal": cmd_steal,
    # ---------------------------
    "eat": cmd_eat,
}


async def process_message(username, content, reply, timestamp):
    print(
        f"{timestamp} - "
        f"{username}: "
        f"{content}"
    )
    
    # We need it for some commands like steal to check for user activity
    update_last_seen(username, int(time()))
    
    if not content.startswith(COMMAND_PREFIX):
        return

    parts = content.split()
    command = parts[0][1:].lower()
    args = parts[1:]

    handler = COMMANDS.get(command)

    if not handler:
        return

    await handler(username, reply, args)