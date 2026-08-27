import random
import time

from utils.users import load_users, set_user
from config import USER_RESPAWN_TIME


SUCCESS_RATE = 0.35
FATAL_FAILURE_RATE = 0.05

MIN_STEAL_BALANCE = 10
STEAL_COOLDOWN = 30 * 60
ACTIVE_TIME_LIMIT = 15 * 60

COOLDOWN_IMMUNITY = ["the_kekbot"]  # Testing


async def cmd_steal(username, reply, args=None):
    print(f"@{username} requested steal command with args: {args}")

    if not args:
        await reply(
            f"@{username} Usage: $steal <target_username>"
        )
        return

    target_username = args[0].lstrip("@")

    # Can't steal yourself
    if target_username.lower() == username.lower():
        await reply(
            f"@{username} You cannot steal from yourself KEKWhat"
        )
        return

    users = load_users()

    # Find thief
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

    current_time = int(time.time())

    # ---------------------------------------------------------
    # THIEF: DEAD CHECK
    # ---------------------------------------------------------

    if user["hp"] <= 0:
        respawn_time = user["death_time"] + USER_RESPAWN_TIME
        remaining = max(0, respawn_time - current_time)

        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        seconds = remaining % 60

        await reply(
            f"@{username} You are dead KEKP | "
            f"You will respawn in "
            f"{f'{hours}h ' if hours else ''}"
            f"{f'{minutes}m ' if minutes else ''}"
            f"{seconds}s"
        )
        return

    # ---------------------------------------------------------
    # MINIMUM BALANCE
    # ---------------------------------------------------------

    if user["balance"] < MIN_STEAL_BALANCE:
        await reply(
            f"@{username} You need at least "
            f"{MIN_STEAL_BALANCE} 🍪 to attempt a steal KEKP"
        )
        return

    # ---------------------------------------------------------
    # COOLDOWN
    # ---------------------------------------------------------

    steal_timer = user.get("steal_timer", 0)

    if (
        current_time < steal_timer
        and username.lower() not in COOLDOWN_IMMUNITY
    ):
        remaining = steal_timer - current_time

        minutes = remaining // 60
        seconds = remaining % 60

        await reply(
            f"@{username} You need to wait before stealing again KEKP "
            f"| Cooldown: "
            f"{f'{minutes}m ' if minutes else ''}"
            f"{seconds}s"
        )
        return

    # ---------------------------------------------------------
    # FIND TARGET
    # ---------------------------------------------------------

    target_user = next(
        (
            user for user in users
            if user["username"].lower() == target_username.lower()
        ),
        None
    )

    if not target_user:
        await reply(
            f"@{username} User '{target_username}' "
            f"not found (didn't use $kek) KEKP"
        )
        return

    # Can't steal from bot
    if target_user["username"].lower() == "the_kekbot":
        await reply(
            f"@{username} You cannot steal from the bot KEKP"
        )
        return

    # ---------------------------------------------------------
    # TARGET: DEAD CHECK
    # ---------------------------------------------------------

    if target_user["hp"] <= 0:
        respawn_time = target_user["death_time"] + USER_RESPAWN_TIME
        remaining = max(0, respawn_time - current_time)

        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        seconds = remaining % 60

        await reply(
            f"@{username} User '{target_user['username']}' is dead KEKP | "
            f"Will respawn in "
            f"{f'{hours}h ' if hours else ''}"
            f"{f'{minutes}m ' if minutes else ''}"
            f"{seconds}s"
        )
        return

    # ---------------------------------------------------------
    # TARGET: ACTIVE CHECK
    # ---------------------------------------------------------

    last_seen = target_user.get("last_seen", 0)

    if last_seen < current_time - ACTIVE_TIME_LIMIT:
        last_seen_text = time.strftime(
            "%d.%m.%Y %H:%M:%S",
            time.localtime(last_seen)
        )

        await reply(
            f"@{username} User '{target_user['username']}' "
            f"was not active in the last "
            f"{ACTIVE_TIME_LIMIT // 60} minutes "
            f"(last seen {last_seen_text} CEST) KEKP"
        )
        return

    # ---------------------------------------------------------
    # TARGET: NO MONEY
    # ---------------------------------------------------------

    if target_user["balance"] <= 0:
        await reply(
            f"@{username} @{target_user['username']} "
            f"has no 🍪 to steal KEKP"
        )
        return

    # ---------------------------------------------------------
    # STEAL AMOUNT
    # ---------------------------------------------------------

    max_steal = min(
        user["balance"] * 2,
        target_user["balance"]
    )

    amount = random.randint(1, max_steal)

    # Start cooldown
    user["steal_timer"] = current_time + STEAL_COOLDOWN

    # ---------------------------------------------------------
    # SUCCESS
    # ---------------------------------------------------------

    success = random.random() < SUCCESS_RATE

    if success:
        # Damage is randomly chosen from 10 to target's current HP
        damage = random.randint(
            min(10, target_user["hp"]),
            target_user["hp"]
        )

        target_user["hp"] -= damage

        # TARGET DIES
        if target_user["hp"] <= 0:
            dropped_keks = target_user["balance"]

            target_user["balance"] = 0
            target_user["hp"] = 0
            target_user["death_time"] = current_time

            user["balance"] += dropped_keks

            set_user(target_user["username"], target_user)
            set_user(user["username"], user)

            await reply(
                f"@{username} Deals {damage} damage to "
                f"{target_user['username']}, killing them and "
                f"taking all +{dropped_keks} 🍪 KEKP"
            )

        # TARGET SURVIVES
        else:
            target_user["balance"] -= amount
            user["balance"] += amount

            set_user(target_user["username"], target_user)
            set_user(user["username"], user)

            await reply(
                f"@{username} Deals {damage} damage to "
                f"{target_user['username']}, knocking them out and "
                f"steals +{amount} 🍪 KEKP"
            )

    # ---------------------------------------------------------
    # FAILURE
    # ---------------------------------------------------------

    else:
        penalty = amount // 2
        penalty = min(
            penalty,
            user["balance"]
        )

        user["balance"] -= penalty

        # 5% chance to instantly kill the thief
        if random.random() < FATAL_FAILURE_RATE:
            damage = user["hp"]
        else:
            # Damage is randomly chosen from 10 to thief's current HP
            damage = random.randint(
                min(10, user["hp"]),
                user["hp"]
            )

        user["hp"] -= damage

        # THIEF DIES
        if user["hp"] <= 0:
            # Thief drops ALL remaining keks
            dropped_keks = user["balance"]

            user["balance"] = 0
            user["hp"] = 0
            user["death_time"] = current_time

            target_user["balance"] += dropped_keks

            set_user(user["username"], user)
            set_user(target_user["username"], target_user)

            await reply(
                f"@{username} Got caught stealing from "
                f"{target_user['username']}, took -{damage} damage and died, "
                f"dropping all -{dropped_keks} 🍪 KEKP"
            )

        # THIEF SURVIVES
        else:
            set_user(user["username"], user)

            await reply(
                f"@{username} Got caught stealing from "
                f"{target_user['username']}, took -{damage} damage "
                f"and lost -{penalty} 🍪 KEKP"
            )