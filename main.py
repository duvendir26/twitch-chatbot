import os
import logging

from dotenv import load_dotenv
from twitchio.ext import commands

from handler import process_message

load_dotenv()

logging.basicConfig(level=logging.INFO)


class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=os.getenv("TWITCH_TOKEN"),
            client_id=os.getenv("TWITCH_CLIENT_ID"),
            prefix="$",
            initial_channels=[
                os.getenv("TWITCH_CHANNEL")
            ]
        )

    async def event_ready(self):
        print(f"Connected as {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        await process_message(
            message.author.name,
            message.content,
            message.channel.send
        )


if __name__ == "__main__":
    bot = TwitchBot()
    bot.run()