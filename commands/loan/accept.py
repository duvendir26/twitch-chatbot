import time

from commands.loan.requests import loan_requests, purge_expired_requests
from utils.loans import load_loans, save_loans
from utils.users import find_user, load_users, reply_if_dead, reply_if_not_registered, set_user


async def cmd_accept_loan(username, reply, args=None):
    print(f"@{username} requested acceptloan command with args: {args}")

    _ = args
    current_time = int(time.time())
    purge_expired_requests(current_time)
    request = next(
        (
            pending for pending in loan_requests
            if pending["borrower"].lower() == username.lower()
        ),
        None,
    )

    if request is None:
        await reply(f"@{username} You have no pending loan offer KEKP")
        return

    loan_requests.remove(request)

    users = load_users()
    lender = find_user(users, request["lender"])
    borrower = find_user(users, request["borrower"])

    if await reply_if_not_registered(reply, username, borrower):
        return

    if await reply_if_not_registered(reply, username, lender, target=request["lender"]):
        return

    if await reply_if_dead(reply, username, borrower, is_self=True):
        return

    if await reply_if_dead(reply, username, lender, is_self=False):
        return

    amount = request["amount"]
    if lender["balance"] < amount:
        await reply(
            f"@{username} {lender['username']} no longer has enough 🍪 KEKP"
        )
        return

    lender["balance"] -= amount
    borrower["balance"] += amount

    loans = load_loans()
    loans.append({
        "lender": lender["username"],
        "borrower": borrower["username"],
        "principal": amount,
        "repaid": 0,
        "created_at": current_time,
    })

    set_user(lender["username"], lender)
    set_user(borrower["username"], borrower)
    save_loans(loans)

    await reply(
        f"@{username} accepted {lender['username']}'s loan | "
        f"Change: +{amount} 🍪 KEKP"
    )