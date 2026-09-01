# Loan system for all players
# Ask for loan, accept
# Repay loan
# How to prevent loan abuse (players taking out loans and not repaying them)
# Could implement a system where players have to pay back loans with interest, and if they fail to repay, they could face penalties such as reduced credit score or limited access to future loans. Additionally, there could be a maximum loan limit based on the player's in-game performance or reputation.
# 1 hour time to repay a loan with fixed interest but after that it will increase and player that gave loan can use a command to collect the loan or wait for interest to build up
# Player that loaned has a command to repay the loan 
# There is also a command to see your loans and for people to see how much they are owed 
# so commands loan, repay, collect, loans (shows both your loans and loans owed to you)

import json
from time import time


from config import COMMAND_PREFIX
from utils.users import find_user, load_users, reply_if_dead, reply_if_not_registered, set_user
from utils.loans import load_loans, save_loans
from utils.amounts import parse_positive_amount

GRACE_PERIOD = 60 * 60           # 1 hour to repay before interest starts
INTEREST_RATE = 0.1              # compounding rate per interval once overdue
INTEREST_INTERVAL = 60 * 60      # interest compounds hourly
MAX_ACTIVE_LOANS_PER_BORROWER = 3


def _find_loan(loans, lender, borrower):
    return next(
        (
            loan for loan in loans
            if loan["lender"].lower() == lender.lower()
            and loan["borrower"].lower() == borrower.lower()
        ),
        None
    )


def _loans_lent_by(loans, username):
    return [loan for loan in loans if loan["lender"].lower() == username.lower()]


def _loans_owed_by(loans, username):
    return [loan for loan in loans if loan["borrower"].lower() == username.lower()]


def _amount_owed(loan, now=None):
    """Outstanding balance on `loan`: principal (+ compounding interest once overdue) minus repayments."""
    now = now if now is not None else time()
    overdue = now - (loan["created_at"] + GRACE_PERIOD)

    if overdue <= 0:
        total = loan["principal"]
    else:
        periods = overdue / INTEREST_INTERVAL
        total = loan["principal"] * (1 + INTEREST_RATE) ** periods

    return max(0, round(total - loan["repaid"]))


async def cmd_loan(username, reply, args=None):
    print(f"@{username} requested loan command with args: {args}")

    args = args or []

    if len(args) < 2:
        await reply(
            f"@{username} Usage: "
            f"{COMMAND_PREFIX}loan <borrower> <amount>"
        )
        return

    borrower_username = args[0].lstrip('@')

    if borrower_username.lower() == username.lower():
        await reply(
            f"@{username} You cannot loan keks to yourself KEKP"
        )
        return

    users = load_users()
    user = find_user(users, username)

    if await reply_if_not_registered(reply, username, user):
        return

    if await reply_if_dead(reply, username, user, is_self=True):
        return

    borrower = find_user(users, borrower_username)

    if await reply_if_not_registered(
        reply, username, borrower,
        message=f"@{username} User is not registered (has to use {COMMAND_PREFIX}kek to register) wideKEKA"
    ):
        return

    if await reply_if_dead(reply, username, borrower, is_self=False):
        return

    loans = load_loans()

    if _find_loan(loans, username, borrower["username"]):
        await reply(
            f"@{username} You already have an active loan with {borrower['username']} KEKP"
        )
        return

    if len(_loans_owed_by(loans, borrower["username"])) >= MAX_ACTIVE_LOANS_PER_BORROWER:
        await reply(
            f"@{username} {borrower['username']} already has the maximum of "
            f"{MAX_ACTIVE_LOANS_PER_BORROWER} active loans KEKP"
        )
        return

    amount = await parse_positive_amount(
        reply, username, args[1],
        allow_all=True,
        all_amount=user["balance"],
    )
    if amount is None:
        return

    if user["balance"] < amount:
        await reply(
            f"@{username} You don't have enough 🍪 to loan {amount} KEKP"
        )
        return

    current_time = int(time())

    user["balance"] -= amount
    borrower["balance"] += amount

    loans.append({
        "lender": user["username"],
        "borrower": borrower["username"],
        "principal": amount,
        "repaid": 0,
        "created_at": current_time,
    })

    set_user(user["username"], user)
    set_user(borrower["username"], borrower)
    save_loans(loans)

    await reply(
        f"@{username} Loaned {amount} 🍪 to {borrower['username']} | "
        f"Repay within {GRACE_PERIOD // 3600}h to avoid interest KEKP"
    )


async def cmd_repay(username, reply, args=None):
    print(f"@{username} requested repay command with args: {args}")

    args = args or []

    if len(args) < 1:
        await reply(
            f"@{username} Usage: {COMMAND_PREFIX}repay <lender> <amount | all>"
        )
        return

    lender_username = args[0].lstrip('@')

    users = load_users()
    user = find_user(users, username)

    if await reply_if_not_registered(reply, username, user):
        return

    loans = load_loans()
    loan = _find_loan(loans, lender_username, username)

    if loan is None:
        await reply(
            f"@{username} You have no active loan with {lender_username} KEKP"
        )
        return

    owed = _amount_owed(loan)
    amount_arg = args[1] if len(args) > 1 else "all"

    amount = await parse_positive_amount(
        reply, username, amount_arg,
        allow_all=True,
        all_amount=owed,
        cap=owed,
    )
    if amount is None:
        return

    if user["balance"] < amount:
        await reply(
            f"@{username} You don't have enough 🍪 to repay {amount} KEKP"
        )
        return

    lender = find_user(users, lender_username)

    user["balance"] -= amount
    lender["balance"] += amount
    loan["repaid"] += amount

    remaining = _amount_owed(loan)

    if remaining <= 0:
        loans.remove(loan)
        await reply(
            f"@{username} Repaid {amount} 🍪 to {lender['username']} | Loan settled KEKP"
        )
    else:
        await reply(
            f"@{username} Repaid {amount} 🍪 to {lender['username']} | "
            f"Remaining owed: {remaining} 🍪 KEKP"
        )

    set_user(user["username"], user)
    set_user(lender["username"], lender)
    save_loans(loans)


async def cmd_collect(username, reply, args=None):
    print(f"@{username} requested collect command with args: {args}")

    args = args or []

    if len(args) < 1:
        await reply(
            f"@{username} Usage: {COMMAND_PREFIX}collect <borrower>"
        )
        return

    borrower_username = args[0].lstrip('@')

    users = load_users()
    user = find_user(users, username)

    if await reply_if_not_registered(reply, username, user):
        return

    loans = load_loans()
    loan = _find_loan(loans, username, borrower_username)

    if loan is None:
        await reply(
            f"@{username} You have no active loan with {borrower_username} KEKP"
        )
        return

    owed = _amount_owed(loan)
    borrower = find_user(users, borrower_username)

    collected = min(owed, borrower["balance"])

    borrower["balance"] -= collected
    user["balance"] += collected

    loans.remove(loan)

    set_user(user["username"], user)
    set_user(borrower["username"], borrower)
    save_loans(loans)

    if collected < owed:
        await reply(
            f"@{username} Collected {collected} 🍪 from {borrower['username']} "
            f"(they couldn't cover the remaining {owed - collected} 🍪, debt forgiven) KEKP"
        )
    else:
        await reply(
            f"@{username} Collected {collected} 🍪 from {borrower['username']} | Loan settled KEKP"
        )


async def cmd_loans(username, reply, args=None):
    print(f"@{username} requested loans command with args: {args}")

    args = args or []
    target_username = args[0].lstrip('@') if args else username

    loans = load_loans()
    now = time()

    owed = _loans_owed_by(loans, target_username)
    lent = _loans_lent_by(loans, target_username)

    if not owed and not lent:
        await reply(f"@{username} {target_username} has no active loans KEKP")
        return

    parts = []

    if owed:
        owed_text = " | ".join(
            f"{loan['lender']}: {_amount_owed(loan, now)} 🍪"
            for loan in owed
        )
        parts.append(f"Owes: {owed_text}")

    if lent:
        lent_text = " | ".join(
            f"{loan['borrower']}: {_amount_owed(loan, now)} 🍪"
            for loan in lent
        )
        parts.append(f"Owed by others: {lent_text}")

    await reply(f"@{username} {target_username}'s loans - {' | '.join(parts)}")
