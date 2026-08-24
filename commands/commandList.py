COMMAND_LIST_URL = "https://pastebin.com/eGchPPe0" 

async def cmd_command_list(username, reply, args=None):     
    await reply(f"@{username} Full commands list: {COMMAND_LIST_URL}")