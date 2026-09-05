# Players can challenge each other to duels and wager coins on the outcome. The winner will receive the wagered coins and the loser will lose them. The duel system will also keep track of wins and losses for each player.

# If player dies in a duel they will lose their keks

# Simplified for now: 50/50 coin flip (skewed slightly by level) decides the winner, no honor system.

import random
import time

from config import COMMAND_PREFIX
from utils.users import find_user, load_users, reply_if_dead, reply_if_not_registered, set_user
from utils.amounts import parse_positive_amount
from utils.xp import add_xp, get_level

ACTIVE_TIME_LIMIT = 15 * 60
DUEL_REQUEST_TIMEOUT = 30
DUEL_XP_PERCENT = 0.15
DUEL_LOSER_XP_PERCENT = 0.5

# Small edge for the higher-level fighter, capped so it never gets too unbalanced
WIN_CHANCE_PER_LEVEL = 0.015
MAX_WIN_CHANCE_SWING = 0.15
DAMAGE_BONUS_PER_LEVEL = 0.02
MAX_DAMAGE_BONUS = 0.3

# Pending challenges awaiting a $accept, cleared on bot restart
duel_requests = []


def _purge_expired_requests(current_time):
    duel_requests[:] = [
        r for r in duel_requests
        if r["created_at"] + DUEL_REQUEST_TIMEOUT > current_time
    ]


async def cmd_duel(username, reply, args=None):
    print(f"@{username} requested duel command with args: {args}")
    
    args = args or []
    
    if len(args) < 2:
        await reply(
            f"@{username} Usage: "
            f"{COMMAND_PREFIX}duel <opponent> <amount>"
        )
        return
    
    opponent_username = args[0].lstrip('@')

    if opponent_username.lower() == username.lower():
        await reply(
            f"@{username} You cannot duel yourself KEKScreen"
        )
        return
    
    users = load_users()
    user = find_user(users, username)

    if await reply_if_not_registered(reply, username, user):
        return
    
    if await reply_if_dead(reply, username, user, is_self=True):
        return
    
    opponent = find_user(users, opponent_username)

    if await reply_if_not_registered(
        reply, username, opponent,
        message=f"@{username} User is not registered (has to use {COMMAND_PREFIX}kek to register) wideKEKA"
    ):
        return
    
    if await reply_if_dead(reply, username, opponent, is_self=False):
        return

    current_time = int(time.time())

    # Same activity check as steal, so you can't challenge an AFK opponent
    last_seen = opponent.get("last_seen", 0)
    if last_seen < current_time - ACTIVE_TIME_LIMIT:
        last_seen_text = time.strftime(
            "%d.%m.%Y %H:%M:%S",
            time.localtime(last_seen)
        )

        await reply(
            f"@{username} User '{opponent['username']}' "
            f"was not active in the last "
            f"{ACTIVE_TIME_LIMIT // 60} minutes "
            f"(last seen {last_seen_text} CEST) KEKP"
        )
        return

    amount = await parse_positive_amount(
        reply, username, args[1],
        allow_all=True,
        all_amount=min(user["balance"], opponent["balance"]),
    )
    if amount is None:
        return

    if amount > user["balance"]:
        await reply(
            f"@{username} You don't have enough 🍪 KEKScreen"
        )
        return

    if amount > opponent["balance"]:
        await reply(
            f"@{username} {opponent['username']} doesn't have enough 🍪 KEKScreen"
        )
        return

    _purge_expired_requests(current_time)

    user_has_pending_duel = any(
        username.lower() in (request["challenger"].lower(), request["opponent"].lower())
        for request in duel_requests
    )
    if user_has_pending_duel:
        await reply(
            f"@{username} You already have a pending duel challenge KEKP"
        )
        return

    opponent_has_pending_duel = any(
        opponent["username"].lower() in (request["challenger"].lower(), request["opponent"].lower())
        for request in duel_requests
    )
    if opponent_has_pending_duel:
        await reply(
            f"@{username} {opponent['username']} already has a pending duel challenge KEKP"
        )
        return

    duel_requests.append({
        "challenger": user["username"],
        "opponent": opponent["username"],
        "amount": amount,
        "created_at": current_time,
    })

    await reply(
        f"@{opponent['username']} {username} challenges you to a duel for {amount} 🍪 "
        f"type {COMMAND_PREFIX}accept "
        f"(expires in {DUEL_REQUEST_TIMEOUT}s) KEKP"
    )


async def cmd_accept(username, reply, args=None):
    print(f"@{username} requested accept command with args: {args}")

    current_time = int(time.time())
    _purge_expired_requests(current_time)

    pending = [r for r in duel_requests if r["opponent"].lower() == username.lower()]

    if args:
        challenger_arg = args[0].lstrip('@').lower()
        pending = [r for r in pending if r["challenger"].lower() == challenger_arg]

    if not pending:
        await reply(
            f"@{username} You have no pending duel challenges KEKP"
        )
        return

    request = pending[0]
    duel_requests.remove(request)

    users = load_users()
    challenger = find_user(users, request["challenger"])
    opponent = find_user(users, request["opponent"])

    if await reply_if_not_registered(reply, username, opponent):
        return

    if await reply_if_not_registered(reply, username, challenger, target=request["challenger"]):
        return

    if await reply_if_dead(reply, username, opponent, is_self=True):
        return

    if await reply_if_dead(reply, username, challenger, is_self=False):
        return

    amount = request["amount"]

    if amount > challenger["balance"]:
        await reply(
            f"@{username} {challenger['username']} no longer has enough 🍪 KEKScreen"
        )
        return

    if amount > opponent["balance"]:
        await reply(
            f"@{username} You no longer have enough 🍪 KEKScreen"
        )
        return

    await _resolve_duel(challenger, opponent, amount, reply)


async def _resolve_duel(challenger, opponent, amount, reply):
    current_time = int(time.time())

    challenger_level = get_level(challenger.get("xp", 0))
    opponent_level = get_level(opponent.get("xp", 0))
    level_diff = challenger_level - opponent_level

    win_chance_swing = max(
        -MAX_WIN_CHANCE_SWING,
        min(MAX_WIN_CHANCE_SWING, level_diff * WIN_CHANCE_PER_LEVEL)
    )
    challenger_wins = random.random() < 0.5 + win_chance_swing
    winner, loser = (challenger, opponent) if challenger_wins else (opponent, challenger)

    # Damage rolled the same way as steal: 10 up to the loser's current HP
    base_damage = random.randint(min(10, loser["hp"]), loser["hp"])

    # Higher-level winner deals a bit more damage, capped so it stays balanced
    winner_level = get_level(winner.get("xp", 0))
    loser_level = get_level(loser.get("xp", 0))
    damage_bonus = min(
        max(0, winner_level - loser_level) * DAMAGE_BONUS_PER_LEVEL,
        MAX_DAMAGE_BONUS
    )
    damage = min(round(base_damage * (1 + damage_bonus)), loser["hp"])
    bonus_damage = damage - base_damage
    loser["hp"] -= damage

    winner["duel_wins"] += 1
    loser["duel_losses"] += 1

    bonus_text = f" (+{bonus_damage} from level advantage)" if bonus_damage > 0 else ""

    if loser["hp"] <= 0:
        # Loser dies and drops all their keks to the winner
        dropped_keks = loser["balance"]

        loser["balance"] = 0
        loser["hp"] = 0
        loser["death_time"] = current_time

        winner["balance"] += dropped_keks
        keks_won = dropped_keks
    else:
        winner["balance"] += amount
        loser["balance"] -= amount
        keks_won = amount

    xp_reward = round(keks_won * DUEL_XP_PERCENT)
    loser_xp_reward = round(xp_reward * DUEL_LOSER_XP_PERCENT)
    gained_xp = add_xp(winner, xp_reward)
    add_xp(loser, loser_xp_reward)

    set_user(challenger["username"], challenger)
    set_user(opponent["username"], opponent)

    if loser["hp"] <= 0:
        await reply(
            f"@{winner['username']} wins the duel dealing {damage} damage{bonus_text} to {loser['username']}, "
            f"killing them KEK7 | Change: +{keks_won} 🍪 | XP Gain: +{gained_xp} XP"
        )
    else:
        await reply(
            f"@{winner['username']} wins the duel dealing {damage} damage{bonus_text} to {loser['username']} "
            f"| Change: +{keks_won} 🍪 KEKShook | XP Gain: +{gained_xp} XP"
        )
