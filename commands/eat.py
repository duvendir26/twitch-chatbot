from utils.users import find_user, load_users, reply_if_dead, reply_if_not_registered, set_user
from utils.amounts import parse_positive_amount
from config import COMMAND_PREFIX

HEAL_PRICE = 5
MAX_HP = 100


def _usage(username):
    return (
        f"@{username} Usage: {COMMAND_PREFIX}heal (or {COMMAND_PREFIX}eat) <user (optional)> <amount | full> "
        f"({HEAL_PRICE} 🍪 per HP) KEKP"
    )


async def cmd_eat(username, reply, args=None):
    print(f"@{username} requested eat command with args: {args}")

    args = args or []

    # No arguments = show usage
    if len(args) == 0:
        await reply(_usage(username))
        return

    # If only one argument is given, it is the amount (healing self)
    # If two arguments are given, first is the target username, second is the amount
    target_username = username

    if len(args) == 1:
        heal_arg = args[0].lower()
    else:
        target_username = args[0].lstrip("@")
        heal_arg = args[1].lower()

    is_self = target_username.lower() == username.lower()

    users = load_users()

    # The caller always pays for the heal, even when healing someone else
    payer = find_user(users, username)

    if await reply_if_not_registered(reply, username, payer):
        return

    if await reply_if_dead(reply, username, payer, is_self=True):
        return

    target = payer if is_self else find_user(users, target_username)

    if not is_self and await reply_if_not_registered(reply, username, target, target=target_username):
        return

    # Dead users cannot be healed
    if not is_self and await reply_if_dead(reply, username, target, is_self=False):
        return

    # Already full HP
    if target["hp"] >= MAX_HP:
        await reply(
            f"@{username} {target_username} is already at full health KEKP"
        )
        return

    # Determine healing amount
    amount = await parse_positive_amount(
        reply,
        username,
        heal_arg,
        allow_all=True,
        all_amount=MAX_HP - target["hp"],
        cap=MAX_HP - target["hp"],
        invalid_message=_usage(username),
    )
    if amount is None:
        return

    # Calculate total cost
    total_price = amount * HEAL_PRICE

    if payer["balance"] < total_price:
        await reply(
            f"@{username} You don't have enough 🍪 to heal {amount} HP. "
            f"You need {total_price} 🍪 KEKP"
        )
        return

    # Heal and charge
    target["hp"] += amount
    payer["balance"] -= total_price

    set_user(payer["username"], payer)
    if not is_self:
        set_user(target["username"], target)

    if is_self:
        await reply(
            f"@{username} YouCanEatThem | "
            f"Change: -{total_price} 🍪, +{amount} ❤️ | "
            f"Current HP: ❤️ {target['hp']}"
        )
    else:
        await reply(
            f"@{username} Fed {target['username']} | "
            f"Change: -{total_price} 🍪 (you), +{amount} ❤️ ({target['username']}) | "
            f"{target['username']}'s HP: ❤️ {target['hp']}"
        )

