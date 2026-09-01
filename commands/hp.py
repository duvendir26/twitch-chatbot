from utils.users import find_user, hp_bar, load_users, reply_if_dead, reply_if_not_registered


async def cmd_hp(username, reply, args=None):
    print(f"@{username} requested hp command with args: {args}")
    
    if args and len(args) > 0:
        username = args[0]

    users = load_users()
    user = find_user(users, username)

    if await reply_if_not_registered(reply, username, user):
        return

    if await reply_if_dead(reply, username, user, is_self=True):
        return

    await reply(
        f"@{username} [{hp_bar(user['hp'])}] [{user['hp']} HP]"
    )