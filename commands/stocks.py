from random import randint

from utils.stocks import load_stocks, save_stocks
from utils.users import load_users, set_user
from config import COMMAND_PREFIX

MIN_STOCK_PRICE = 5
MAX_STOCK_PRICE = 50

async def cmd_stocks(username, reply, args=None):
    print(f"@{username} requested stocks command with args: {args}")

    stocks = load_stocks()

    stock_list = " | ".join(
        [f"{stock['name']}: {stock['price']} 🍪" for stock in stocks]
    )

    await reply(f"@{username} Stocks: {stock_list}")


async def cmd_portfolio(username, reply, args=None):
    print(f"@{username} requested portfolio command with args: {args}")

    users = load_users()
    stocks = load_stocks()

    user = next(
        (
            user for user in users
            if user["username"].lower() == username.lower()
        ),
        None
    )

    if user is None:
        await reply(
            f"@{username} User not found. Use $kek to register KEKP"
        )
        return

    portfolio = user.get("portfolio", [])

    if not portfolio:
        await reply(f"@{username} Your portfolio is empty KEKP")
        return

    portfolio_list = []
    total_value = 0

    for owned_stock in portfolio:
        stock = next(
            (
                stock for stock in stocks
                if stock["name"].lower() == owned_stock["name"].lower()
            ),
            None
        )

        if stock is None:
            continue

        amount = owned_stock.get("amount", 0)
        value = stock["price"] * amount

        total_value += value

        portfolio_list.append(
            f"{stock['name']}: {amount} "
            f"{'share' if amount == 1 else 'shares'} "
            f"({value} 🍪)"
        )

    if not portfolio_list:
        await reply(f"@{username} Your portfolio is empty KEKP")
        return

    portfolio_text = " | ".join(portfolio_list)

    await reply(
        f"@{username} Portfolio: {portfolio_text} "
        f"| Total Value: {total_value} 🍪"
    )
    
    
async def cmd_buy(username, reply, args=None):
    args = args or []

    if len(args) < 2:
        await reply(
            f"@{username} Usage: "
            f"{COMMAND_PREFIX}buy <stock_name> <amount>"
        )
        return

    stock_name = args[0].lower()
    amount_arg = args[1].lower()

    stocks = load_stocks()

    stock = next(
        (
            stock for stock in stocks
            if stock["name"].lower() == stock_name
        ),
        None
    )

    if stock is None:
        await reply(
            f"@{username} Stock '{stock_name}' does not exist KEKP"
        )
        return

    users = load_users()
    user = next(
        (
            user for user in users
            if user["username"].lower() == username.lower()
        ),
        None
    )

    if user is None:
        await reply(
            f"@{username} User not found. Use $kek to register KEKP"
        )
        return

    portfolio = user.setdefault("portfolio", [])

    owned_stock = next(
        (
            item for item in portfolio
            if item["name"].lower() == stock["name"].lower()
        ),
        None
    )

    current_amount = owned_stock["amount"] if owned_stock else 0
    remaining_limit = 100 - current_amount

    if remaining_limit <= 0:
        await reply(
            f"@{username} You already own the maximum of 100 "
            f"{stock['name']} shares KEKP"
        )
        return

    price = stock["price"]
    balance = user["balance"]

    if amount_arg == "all":
        affordable_amount = balance // price

        amount = min(affordable_amount, remaining_limit)

        if amount <= 0:
            await reply(
                f"@{username} You don't have enough 🍪 to buy "
                f"{stock['name']} KEKP"
            )
            return

    else:
        # Handle number
        try:
            amount = int(amount_arg)
        except ValueError:
            await reply(
                f"@{username} Enter a valid number or 'all' KEKP"
            )
            return

        if amount <= 0:
            await reply(
                f"@{username} Amount must be greater than 0 KEKP"
            )
            return

        if amount > remaining_limit:
            await reply(
                f"@{username} You can only buy {remaining_limit} more "
                f"{stock['name']} shares KEKP"
            )
            return

    total_cost = price * amount

    if balance < total_cost:
        await reply(
            f"@{username} You need {total_cost} 🍪 "
            f"but only have {balance} 🍪 KEKP"
        )
        return

    user["balance"] -= total_cost

    if owned_stock:
        owned_stock["amount"] += amount
    else:
        owned_stock = {
            "name": stock["name"],
            "amount": amount
        }

        portfolio.append(owned_stock)

    set_user(user["username"], user)
    
    portfolio_text = " | ".join(
        f"{item['name']}: {item['amount']} "
        f"{'share' if item['amount'] == 1 else 'shares'}"
        for item in portfolio
        if item.get("amount", 0) > 0
    )

    await reply(
        f"@{username} Bought {amount} "
        f"{'share' if amount == 1 else 'shares'} of {stock['name']} "
        f"| Change: -{total_cost} 🍪 | "
        f"Balance: {user['balance']} 🍪 | "
        f"Portfolio: {portfolio_text}"
    )


async def cmd_sell(username, reply, args=None):
    args = args or []

    if len(args) < 2:
        await reply(
            f"@{username} Usage: "
            f"{COMMAND_PREFIX}sell <stock_name> <amount>"
        )
        return

    stock_name = args[0].lower()
    amount_arg = args[1].lower()

    stocks = load_stocks()

    stock = next(
        (
            stock for stock in stocks
            if stock["name"].lower() == stock_name
        ),
        None
    )

    if stock is None:
        await reply(
            f"@{username} Stock '{stock_name}' does not exist KEKP"
        )
        return

    users = load_users()

    user = next(
        (
            user for user in users
            if user["username"].lower() == username.lower()
        ),
        None
    )

    if user is None:
        await reply(
            f"@{username} User not found. Use $kek to register KEKP"
        )
        return

    portfolio = user.setdefault("portfolio", [])
    owned_stock = next(
        (
            item for item in portfolio
            if item["name"].lower() == stock["name"].lower()
        ),
        None
    )

    if owned_stock is None or owned_stock["amount"] <= 0:
        await reply(
            f"@{username} You don't own any {stock['name']} KEKP"
        )
        return

    owned_amount = owned_stock["amount"]

    if amount_arg == "all":
        amount = owned_amount

    else:
        try:
            amount = int(amount_arg)
        except ValueError:
            await reply(
                f"@{username} Enter a valid number or 'all' KEKP"
            )
            return

        if amount <= 0:
            await reply(
                f"@{username} Amount must be greater than 0 KEKP"
            )
            return

        if amount > owned_amount:
            await reply(
                f"@{username} You only own {owned_amount} "
                f"{stock['name']} shares KEKP"
            )
            return

    price = stock["price"]
    total_value = price * amount

    user["balance"] += total_value

    owned_stock["amount"] -= amount

    if owned_stock["amount"] == 0:
        portfolio.remove(owned_stock)

    set_user(user["username"], user)
    
    portfolio_text = " | ".join(
        f"{item['name']}: {item['amount']} "
        f"{'share' if item['amount'] == 1 else 'shares'}"
        for item in portfolio
        if item.get("amount", 0) > 0
    )

    if not portfolio_text:
        portfolio_text = "Empty"

    await reply(
        f"@{username} Sold {amount} "
        f"{'share' if amount == 1 else 'shares'} of {stock['name']} "
        f"| Change: +{total_value} 🍪 | "
        f"Balance: {user['balance']} 🍪 | "
        f"Portfolio: {portfolio_text}"
    )


def update_stock_prices():
    stocks = load_stocks()

    for stock in stocks:
        stock["price"] = randint(
            MIN_STOCK_PRICE,
            MAX_STOCK_PRICE
        )

    save_stocks(stocks)