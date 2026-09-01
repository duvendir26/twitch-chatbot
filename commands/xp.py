from utils.users import find_user, hp_bar, load_users, reply_if_not_registered
from utils.xp import get_kek_bonus, get_level, get_xp_progress


async def cmd_xp(username, reply, args=None):
    print(f"@{username} requested xp command with args: {args}")

    if args and len(args) > 0:
        username = args[0]

    users = load_users()
    user = find_user(users, username)

    if await reply_if_not_registered(reply, username, user):
        return

    level = get_level(user.get("xp", 0))
    bonus = get_kek_bonus(level)
    xp_progress, xp_needed = get_xp_progress(user.get("xp", 0))
    bar = hp_bar(xp_progress, max_hp=xp_needed, width=10) if xp_needed else "█" * 10
    xp_text = f"{xp_progress}/{xp_needed} XP" if xp_needed else f"{user.get('xp', 0)} XP (MAX)"

    await reply(
        f"@{username} [{bar}] [{xp_text}] [Level: {level}]"
    )
