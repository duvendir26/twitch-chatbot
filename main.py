import os
import asyncio
import logging

from config import STOCK_UPDATE_INTERVAL, COMMAND_PREFIX, USER_RESPAWN_TIME
from dotenv import load_dotenv
from twitchio.ext import commands
from handler import process_message
from commands.stocks import update_stock_prices

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class TwitchBot(commands.Bot):
    def __init__(self):
        channels = [
            channel.strip()
            for channel in os.getenv("TWITCH_CHANNEL", "").split(",")
            if channel.strip()
        ]

        super().__init__(
            token=os.getenv("TWITCH_TOKEN"),
            prefix=COMMAND_PREFIX,
            initial_channels=channels
        )

    async def event_ready(self):
        print(f"Connected as {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        await process_message(
            message.author.name,
            message.content,
            message.channel.send,
            message.timestamp
        )


async def stock_runner():
    while True:
        try:
            update_stock_prices()
            logging.info("Stock prices updated")
        except Exception:
            logging.exception("Error updating stock prices")

        await asyncio.sleep(STOCK_UPDATE_INTERVAL)
        # await asyncio.sleep(1)  # testing


async def respawn_checker(bot):
    while True:
        try:
            from utils.users import load_users, set_user
            from time import time

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
                            f"@{user['username']} has respawned with 25 HP KEKP"
                        )

        except Exception:
            logging.exception("Error checking respawn times")

        await asyncio.sleep(10)


async def main():
    asyncio.create_task(stock_runner())

    while True:
        bot = TwitchBot()

        respawn_task = asyncio.create_task(
            respawn_checker(bot)
        )

        try:
            await bot.start()

        except Exception:
            logging.exception(
                "Twitch connection lost. Reconnecting in 10 seconds..."
            )

        finally:
            respawn_task.cancel()

            try:
                await bot.close()
            except Exception:
                pass

        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())