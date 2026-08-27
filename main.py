import os
import asyncio
import logging

from config import STOCK_UPDATE_INTERVAL, COMMAND_PREFIX, USER_RESPAWN_TIME
from dotenv import load_dotenv
from twitchio.ext import commands
from handler import process_message
from runners.respawn import respawn_runner
from runners.stock import stock_runner

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


async def main():
    asyncio.create_task(stock_runner())

    while True:
        bot = TwitchBot()

        respawn_task = asyncio.create_task(
            respawn_runner(bot)
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