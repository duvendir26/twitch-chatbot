from config import COMMAND_PREFIX
from utils.users import find_user, hp_bar, load_users, reply_if_dead, reply_if_not_registered, set_user

RESURRECT_COST = 500
RESURRECT_HP = 25


async def cmd_resurrect(username, reply, args=None):
    print(f"@{username} requested resurrect command with args: {args}")

    args = args or []

    if not args:
        await reply(f"@{username} Usage: {COMMAND_PREFIX}res <user>")
        return

    target_username = args[0].lstrip("@")

    if target_username.lower() == username.lower():
        await reply(f"@{username} You cannot resurrect yourself KEKInsane")
        return

    users = load_users()
    user = find_user(users, username)
    target = find_user(users, target_username)

    if await reply_if_not_registered(reply, username, user):
        return

    if await reply_if_dead(reply, username, user, is_self=True):
        return

    if await reply_if_not_registered(reply, username, target, target=target_username):
        return

    if target["hp"] > 0:
        await reply(f"@{username} {target['username']} is already alive KEKWhat")
        return

    if user["balance"] < RESURRECT_COST:
        await reply(
            f"@{username} You need {RESURRECT_COST} 🍪 wideKEKA"
        )
        return

    user["balance"] -= RESURRECT_COST
    target["hp"] = RESURRECT_HP
    target["death_time"] = 0

    set_user(user["username"], user)
    set_user(target["username"], target)

    await reply(
        f"@{username} resurrected {target['username']} KEKInsane | "
        f"Change: -{RESURRECT_COST} 🍪"
    )