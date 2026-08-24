from utils.users import load_users



async def cmd_bottom(username, reply, args=None):
    print(f"@{username} requested bottom command with args: {args}")

    users = load_users()
    sorted_users = sorted(
            users,
            key=lambda user: user["balance"],
            reverse=False
        )

    leaderboard_message = "Bottom 10 users: "
    for i, user in enumerate(sorted_users[:10], start=1):
        separator = "" if i == 1 else " | "
        
        leaderboard_message += (
            f"{separator}{i}. "
            f"{user['username']}: "
            f"{user['balance']} 🍪"
        )

    await reply(leaderboard_message)