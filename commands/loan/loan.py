import time

from commands.loan.requests import LOAN_REQUEST_TIMEOUT, has_pending_offer, loan_requests, purge_expired_requests
from config import COMMAND_PREFIX
from utils.amounts import parse_positive_amount
from utils.users import find_user, load_users, reply_if_dead, reply_if_not_registered


async def cmd_loan(username, reply, args=None):
    print(f"@{username} requested loan command with args: {args}")

    args = args or []

    if len(args) < 2:
        await reply(
            f"@{username} Usage: {COMMAND_PREFIX}loan <borrower> <amount>"
        )
        return

    borrower_username = args[0].lstrip("@")

    if borrower_username.lower() == username.lower():
        await reply(f"@{username} You cannot loan keks to yourself KEKP")
        return

    users = load_users()
    lender = find_user(users, username)
    borrower = find_user(users, borrower_username)

    if await reply_if_not_registered(reply, username, lender):
        return

    if await reply_if_dead(reply, username, lender, is_self=True):
        return

    if await reply_if_not_registered(reply, username, borrower, target=borrower_username):
        return

    if await reply_if_dead(reply, username, borrower, is_self=False):
        return

    amount = await parse_positive_amount(
        reply, username, args[1], allow_all=True, all_amount=lender["balance"]
    )
    if amount is None:
        return

    if lender["balance"] < amount:
        await reply(
            f"@{username} You don't have enough 🍪 to loan {amount} KEKP"
        )
        return

    current_time = int(time.time())
    purge_expired_requests(current_time)

    if has_pending_offer(lender["username"]) or has_pending_offer(borrower["username"]):
        await reply(f"@{username} One of you already has a pending loan offer KEKP")
        return

    loan_requests.append({
        "lender": lender["username"],
        "borrower": borrower["username"],
        "amount": amount,
        "created_at": current_time,
    })

    await reply(
        f"@{borrower['username']} {lender['username']} offers you a loan of "
        f"{amount} 🍪 | Type {COMMAND_PREFIX}acceptloan within "
        f"{LOAN_REQUEST_TIMEOUT}s KEKP"
    )