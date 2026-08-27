import asyncio
import logging

from utils.users import load_users, set_user
from time import time
from config import USER_RESPAWN_TIME

async def respawn_runner(bot):
    while True:
        try:
            users = load_users()
            current_time = int(time())

            for user in users:
                if (
                    user["hp"] <= 0
                    and current_time >= user["death_time"] + USER_RESPAWN_TIME
                ):
                    user["hp"] = 25
                    user["death_time"] = 0

                    set_user(user["username"], user)

                    logging.info(
                        f"User '{user['username']}' has respawned with 25 HP"
                    )

                    for channel in bot.connected_channels:
                        await channel.send(
                            f"@{user['username']} You have respawned with ❤️ 25 KEKP"
                        )

        except Exception:
            logging.exception("Error checking respawn times")

        await asyncio.sleep(10)