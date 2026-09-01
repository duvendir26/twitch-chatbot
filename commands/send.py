from config import COMMAND_PREFIX
from utils.users import find_user, load_users, reply_if_dead, reply_if_not_registered, set_user
from utils.amounts import parse_positive_amount


async def cmd_send(username, reply, args=None):
    print(f"@{username} requested send command with args: {args}")

    if not args or len(args) < 2:
        await reply(
            f"@{username} Usage: "
            f"{COMMAND_PREFIX}send <recipient> <amount>"
        )
        return

    recipient = args[0].lstrip('@')
    amount_arg = args[1].lower()

    users = load_users()

    user = find_user(users, username)

    if await reply_if_not_registered(reply, username, user):
        return
    
    if await reply_if_dead(reply, username, user, is_self=True):
        return

    recipient_user = find_user(users, recipient)

    if await reply_if_not_registered(
        reply, username, recipient_user,
        message=f"@{username} User is not registered (has to use $kek) wideKEKA"
    ):
        return

    if user["username"].lower() == recipient_user["username"].lower():
        await reply(
            f"@{username} You cannot send keks to yourself KEKP"
        )
        return
    
    if await reply_if_dead(reply, username, recipient_user, is_self=False):
        return

    amount = await parse_positive_amount(
        reply,
        username,
        amount_arg,
        allow_all=True,
        all_amount=user["balance"],
        invalid_message=f"@{username} Invalid amount. Please enter a valid number or 'all' KEKP",
        zero_message=f"@{username} Amount must be greater than zero KEKP",
    )
    if amount is None:
        return

    if user["balance"] < amount:
        await reply(
            f"@{username} You do not have enough keks to send KEKP"
        )
        return

    user["balance"] -= amount
    recipient_user["balance"] += amount

    set_user(user["username"], user)
    set_user(recipient_user["username"], recipient_user)

    await reply(
        f"@{username} sent {amount} 🍪 "
        f"to @{recipient_user['username']} KEKP "
    )