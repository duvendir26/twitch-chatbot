from utils.users import load_users


async def cmd_leaderboard(username, reply, args=None):
    print(f"@{username} requested leaderboard command with args: {args}")

    users = load_users()

    sorted_users = sorted(
        users,
        key=lambda user: user["balance"],
        reverse=True
    )

    leaderboard_message = "Top 10 kekkers KEKInsane : "
    for i, user in enumerate(sorted_users[:10], start=1):
        separator = "" if i == 1 else " | "
        
        if i == 1:
            leaderboard_message += (
                f"{separator} 👑 "
                f"{user['username']}: "
                f"{user['balance']} 🍪"
            )
        elif i == 2:
            leaderboard_message += (
                f"{separator} 🥈 "
                f"{user['username']}: "
                f"{user['balance']} 🍪"
            )
        elif i == 3:
            leaderboard_message += (
                f"{separator} 🥉 "
                f"{user['username']}: "
                f"{user['balance']} 🍪"
            )
        else:
            leaderboard_message += (
                f"{separator}{i}. "
                f"{user['username']}: "
                f"{user['balance']} 🍪"
            )

    await reply(leaderboard_message)