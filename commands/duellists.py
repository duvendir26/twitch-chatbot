from utils.users import load_users


async def cmd_duellists(username, reply, args=None):
    print(f"@{username} requested duellists command with args: {args}")

    users = load_users()

    sorted_users = sorted(
        users,
        key=lambda user: user.get("duel_wins", 0),
        reverse=True
    )

    leaderboard_message = "Top 10 duellists: "
    for i, user in enumerate(sorted_users[:10], start=1):
        separator = "" if i == 1 else " | "
        wins = user.get("duel_wins", 0)
        losses = user.get("duel_losses", 0)
        total = wins + losses
        winrate = (wins / total * 100) if total > 0 else 0.0

        if i == 1:
            leaderboard_message += (
                f"{separator} 👑 "
                f"{user['username']}: "
                f"{wins} wins ({winrate:.1f}%)"
            )
        elif i == 2:
            leaderboard_message += (
                f"{separator} 🥈 "
                f"{user['username']}: "
                f"{wins} wins ({winrate:.1f}%)"
            )
        elif i == 3:
            leaderboard_message += (
                f"{separator} 🥉 "
                f"{user['username']}: "
                f"{wins} wins ({winrate:.1f}%)"
            )
        else:
            leaderboard_message += (
                f"{separator}{i}. "
                f"{user['username']}: "
                f"{wins} wins ({winrate:.1f}%)"
            )

    await reply(leaderboard_message)
