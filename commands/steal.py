import random
import time

from utils.users import find_user, load_users, reply_if_dead, reply_if_not_registered, set_user
from utils.duration import format_duration
from utils.xp import add_xp, apply_kek_multiplier


SUCCESS_RATE = 0.35

MIN_STEAL_BALANCE = 10
STEAL_COOLDOWN = 30 * 60
ACTIVE_TIME_LIMIT = 15 * 60
STEAL_XP_REWARD = 25

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
    # ---------------------------------------------------------
    # FIND THIEF
    # ---------------------------------------------------------
    
    user = find_user(users, username)

    if await reply_if_not_registered(reply, username, user):
        return

    # ---------------------------------------------------------
    # THIEF: DEAD CHECK
    # ---------------------------------------------------------
    
    current_time = int(time.time())
    if await reply_if_dead(reply, username, user, is_self=True):
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

    #! ---------------------------------------------------------
    #! COOLDOWN
    #! ---------------------------------------------------------

    steal_timer = user.get("steal_timer", 0)
    if (
        current_time < steal_timer
        and username.lower() not in COOLDOWN_IMMUNITY
    ):
        cooldown = format_duration(steal_timer - current_time)

        await reply(
            f"@{username} You need to wait before stealing again KEKP "
            f"| Cooldown: {cooldown}"
        )
        return

    # ---------------------------------------------------------
    # FIND TARGET
    # ---------------------------------------------------------

    target_user = find_user(users, target_username)

    if await reply_if_not_registered(
        reply, username, target_user,
        message=f"@{username} User '{target_username}' not found (didn't use $kek) KEKP"
    ):
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

    if await reply_if_dead(reply, username, target_user, is_self=False):
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

            add_xp(user, STEAL_XP_REWARD)
            reward = apply_kek_multiplier(user, dropped_keks)
            user["balance"] += reward

            set_user(target_user["username"], target_user)
            set_user(user["username"], user)

            await reply(
                f"@{username} Deals {damage} damage to "
                f"{target_user['username']}, killing them and "
                f"taking all +{reward} 🍪 KEKP"
            )

        # TARGET SURVIVES
        else:
            target_user["balance"] -= amount

            add_xp(user, STEAL_XP_REWARD)
            reward = apply_kek_multiplier(user, amount)
            user["balance"] += reward

            set_user(target_user["username"], target_user)
            set_user(user["username"], user)

            await reply(
                f"@{username} Deals {damage} damage to "
                f"{target_user['username']}, knocking them out and "
                f"steals +{reward} 🍪 KEKP"
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
                f"dropping all -{dropped_keks + penalty} 🍪 KEKP"
            )

        # THIEF SURVIVES
        else:
            set_user(user["username"], user)

            await reply(
                f"@{username} Got caught stealing from "
                f"{target_user['username']}, took -{damage} damage "
                f"and lost -{penalty} 🍪 KEKP"
            )