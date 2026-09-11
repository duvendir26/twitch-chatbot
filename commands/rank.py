from utils.users import load_users
from utils.xp import get_level, get_xp_progress


async def cmd_rank(username, reply, args=None):
    print(f"@{username} requested rank command with args: {args}")

    users = load_users()

    # Sorting by xp also breaks level ties by whoever has more xp within that level
    sorted_users = sorted(
        users,
        key=lambda user: user.get("xp", 0),
        reverse=True
    )

    leaderboard_message = "Top 10 ranks: "
    for i, user in enumerate(sorted_users[:10], start=1):
        separator = "" if i == 1 else " | "
        xp = user.get("xp", 0)
        level = get_level(xp)
        progress, needed = get_xp_progress(xp)
        xp_text = f" ({progress}/{needed} XP)" if needed else ""

        if i == 1:
            leaderboard_message += (
                f"{separator} 👑 "
                f"{user['username']}: "
                f"Level {level}{xp_text}"
            )
        elif i == 2:
            leaderboard_message += (
                f"{separator} 🥈 "
                f"{user['username']}: "
                f"Level {level}{xp_text}"
            )
        elif i == 3:
            leaderboard_message += (
                f"{separator} 🥉 "
                f"{user['username']}: "
                f"Level {level}{xp_text}"
            )
        else:
            leaderboard_message += (
                f"{separator}{i}. "
                f"{user['username']}: "
                f"Level {level}{xp_text}"
            )

    await reply(leaderboard_message)
