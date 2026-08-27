import asyncio
import logging

from commands.stocks import update_stock_prices
from config import STOCK_UPDATE_INTERVAL


async def stock_runner():
    while True:
        try:
            update_stock_prices()
            logging.info("Stock prices updated")
        except Exception:
            logging.exception("Error updating stock prices")

        await asyncio.sleep(STOCK_UPDATE_INTERVAL)
        # await asyncio.sleep(1)  # testing