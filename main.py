import os
import logging

from dotenv import load_dotenv
from twitchio.ext import commands

from handler import process_message

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
            prefix="$",
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


if __name__ == "__main__":
    bot = TwitchBot()
    bot.run()