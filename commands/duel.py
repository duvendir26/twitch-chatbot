# Players can challenge each other to duels and wager coins on the outcome. The winner will receive the wagered coins and the loser will lose them. The duel system will also keep track of wins and losses for each player.

# If player dies in a duel they will lose their keks

# Simplified for now: 50/50 coin flip decides the winner, no activity-penalty/honor system.

import random
import time

from config import COMMAND_PREFIX
from utils.users import find_user, load_users, reply_if_dead, reply_if_not_registered, set_user
from utils.amounts import parse_positive_amount
from utils.xp import add_xp, get_level

ACTIVE_TIME_LIMIT = 15 * 60
DUEL_XP_REWARD = 50

# Small edge for the higher-level fighter, capped so it never gets too unbalanced
WIN_CHANCE_PER_LEVEL = 0.015
MAX_WIN_CHANCE_SWING = 0.15
DAMAGE_BONUS_PER_LEVEL = 0.02
MAX_DAMAGE_BONUS = 0.3

duel_requests = []

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

    # Same activity check as steal, so you can't duel an AFK opponent
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
            f"@{username} {opponent['username']} doesn't have enough 🍪 "
            f"to cover that wager KEKScreen"
        )
        return

    challenger_level = get_level(user.get("xp", 0))
    opponent_level = get_level(opponent.get("xp", 0))
    level_diff = challenger_level - opponent_level

    win_chance_swing = max(
        -MAX_WIN_CHANCE_SWING,
        min(MAX_WIN_CHANCE_SWING, level_diff * WIN_CHANCE_PER_LEVEL)
    )
    challenger_wins = random.random() < 0.5 + win_chance_swing
    winner, loser = (user, opponent) if challenger_wins else (opponent, user)

    # Damage rolled the same way as steal: 10 up to the loser's current HP
    damage = random.randint(min(10, loser["hp"]), loser["hp"])

    # Higher-level winner deals a bit more damage, capped so it stays balanced
    winner_level = get_level(winner.get("xp", 0))
    loser_level = get_level(loser.get("xp", 0))
    damage_bonus = min(
        max(0, winner_level - loser_level) * DAMAGE_BONUS_PER_LEVEL,
        MAX_DAMAGE_BONUS
    )
    damage = min(round(damage * (1 + damage_bonus)), loser["hp"])
    loser["hp"] -= damage

    winner["duel_wins"] += 1
    loser["duel_losses"] += 1

    add_xp(winner, DUEL_XP_REWARD)

    if loser["hp"] <= 0:
        # Loser dies and drops all their keks to the winner
        dropped_keks = loser["balance"]

        loser["balance"] = 0
        loser["hp"] = 0
        loser["death_time"] = current_time

        winner["balance"] += dropped_keks

        set_user(user["username"], user)
        set_user(opponent["username"], opponent)

        await reply(
            f"@{winner['username']} deals {damage} damage to {loser['username']}, "
            f"killing them and taking all +{dropped_keks} 🍪 KEKP"
        )
    else:
        winner["balance"] += amount
        loser["balance"] -= amount

        set_user(user["username"], user)
        set_user(opponent["username"], opponent)

        await reply(
            f"@{winner['username']} deals {damage} damage to {loser['username']} "
            f"and wins the duel | Change: +{amount} 🍪 KEKP"
        )
