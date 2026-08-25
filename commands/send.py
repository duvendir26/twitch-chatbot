from config import COMMAND_PREFIX
from utils.users import load_users, set_user


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

    user = next(
        (
            u for u in users
            if u["username"].lower() == username.lower()
        ),
        None
    )

    if not user:
        await reply(
            f"@{username} You are not registered. "
            f"Use $kek to register KEKP"
        )
        return

    recipient_user = next(
        (
            u for u in users
            if u["username"].lower() == recipient.lower()
        ),
        None
    )

    if not recipient_user:
        await reply(
            f"@{username} User is not registered "
            f"(has to use $kek) wideKEKA"
        )
        return

    if user["username"].lower() == recipient_user["username"].lower():
        await reply(
            f"@{username} You cannot send keks to yourself KEKP"
        )
        return

    if amount_arg == "all":
        amount = user["balance"]

    else:
        try:
            amount = int(amount_arg)
        except ValueError:
            await reply(
                f"@{username} Invalid amount. "
                f"Please enter a valid number or 'all' KEKP"
            )
            return

    if amount <= 0:
        await reply(
            f"@{username} Amount must be greater than zero KEKP"
        )
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