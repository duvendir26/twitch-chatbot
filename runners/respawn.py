import asyncio
import logging

from utils.users import hp_bar, load_users, set_user, users_lock, xp_bar
from utils.xp import get_level, get_xp_progress
from time import time
from config import USER_RESPAWN_TIME

async def respawn_runner(bot):
    while True:
        try:
            respawned = []

            async with users_lock:
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
                        respawned.append(user)

                        logging.info(
                            f"User '{user['username']}' has respawned with 25 HP"
                        )

            for user in respawned:
                xp = user.get("xp", 0)
                level = get_level(xp)
                progress, needed = get_xp_progress(xp)

                for channel in bot.connected_channels:
                    await channel.send(
                        f"@{user['username']} respawned KEKP | HP: [{hp_bar(user['hp'])}] [25/100] | XP: [{xp_bar(xp)}] [{progress}/{needed if needed else '✓'}] [Level: {level}]"
                    )

        except Exception:
            logging.exception("Error checking respawn times")

        await asyncio.sleep(10)

        await asyncio.sleep(10)