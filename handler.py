from commands.bonus import cmd_bonus
from commands.coinflip import cmd_coinflip
from commands.leaderboard import cmd_leaderboard
from commands.bottom import cmd_bottom
from commands.stats import cmd_stats
from commands.commandList import cmd_command_list
from commands.send import cmd_send

from config import COMMAND_PREFIX

COMMANDS = {
    "kek": cmd_bonus,
    "bonus": cmd_bonus, #? ALIAS
    "coinflip": cmd_coinflip,
    "leaderboard": cmd_leaderboard,
    "stats": cmd_stats,
    "bottom": cmd_bottom,
    "commands": cmd_command_list,
    "send": cmd_send,
    "give": cmd_send, #? ALIAS
}


async def process_message(username, content, reply, timestamp):
    print(
        f"{timestamp} - "
        f"{username}: "
        f"{content}"
    )
    
    if not content.startswith(COMMAND_PREFIX):
        return

    parts = content.split()
    command = parts[0][1:].lower()
    args = parts[1:]

    handler = COMMANDS.get(command)

    if not handler:
        return

    await handler(username, reply, args)