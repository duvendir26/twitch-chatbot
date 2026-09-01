from utils.duration import format_duration
from utils.users import load_users, respawn_remaining


async def cmd_graveyard(username, reply, args=None):
    print(f"@{username} requested graveyard command with args: {args}")

    users = load_users()
    dead_users = [user for user in users if user["hp"] <= 0]

    if not dead_users:
        await reply(f"@{username} Graveyard is empty, everyone is alive KEKP")
        return

    dead_users.sort(key=respawn_remaining)

    graveyard_list = " | ".join(
        f"{user['username']} (respawns in {format_duration(respawn_remaining(user))})"
        for user in dead_users
    )

    await reply(f"@{username} Graveyard: {graveyard_list}")
