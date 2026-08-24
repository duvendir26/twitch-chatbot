from commands.daily import cmd_daily

COMMAND_PREFIX = "$"

COMMANDS = {
    "kek": cmd_daily,
    "daily": cmd_daily #? ALIAS
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