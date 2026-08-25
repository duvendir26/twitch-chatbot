import random
import time

from utils.users import load_users, set_user

SUCCESS_RATE = 0.25
MIN_STEAL_BALANCE = 10
STEAL_COOLDOWN = 30 * 60
COOLDOWN_IMMUNITY = ["the_kekbot"] #? FOR TESTING


async def cmd_steal(username, reply, args=None):
    print(f"@{username} requested steal command with args: {args}")

    if not args:
        await reply(
            f"@{username} Usage: $steal <target_username>"
        )
        return

    target_username = args[0]
    if target_username.lower() == username.lower():
        await reply(
            f"@{username} You cannot steal from yourself!"
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

    if not user:
        await reply(
            f"@{username} You are not registered. "
            f"Use $kek to register KEKP"
        )
        return

    if user["balance"] < MIN_STEAL_BALANCE:
        await reply(
            f"@{username} You need at least "
            f"{MIN_STEAL_BALANCE} 🍪 to attempt a steal KEKP"
        )
        return

    current_time = int(time.time())
    steal_timer = user.get("steal_timer", 0)
    if current_time < steal_timer and username.lower() not in COOLDOWN_IMMUNITY:
        remaining = steal_timer - current_time
        minutes = remaining // 60
        seconds = remaining % 60

        await reply(
            f"@{username} You need to wait "
            f"before stealing again KEKP | Cooldown: {(str(minutes) + 'm' if minutes > 0 else '')} {seconds}s "
        )
        return

    target_user = next(
        (
            user for user in users
            if user["username"].lower() == target_username.lower()
        ),
        None
    )

    if not target_user:
        await reply(
            f"@{username} Target user '{target_username}' "
            f"not found (didn't use $kek) KEKP"
        )
        return

    if target_user["balance"] <= 0:
        await reply(
            f"@{username} @{target_user['username']} has no 🍪 to steal KEKP"
        )
        return

    max_steal = min(
        user["balance"] * 2,
        target_user["balance"]
    )

    amount = random.randint(1, max_steal)

    user["steal_timer"] = current_time + STEAL_COOLDOWN

    success = random.random() < SUCCESS_RATE
    if success:
        target_user["balance"] -= amount
        user["balance"] += amount

        set_user(target_user["username"], target_user)
        set_user(user["username"], user)

        await reply(
            f"@{username} Stole {amount} 🍪 "
            f"from {target_user['username']} KEKP "
        )

    else:
        penalty = amount // 2
        penalty = min(penalty, user["balance"])

        user["balance"] -= penalty

        set_user(user["username"], user)

        await reply(
            f"@{username} Failed to steal from "
            f"{target_user['username']} and lost -{penalty} 🍪 KEKP"
        )