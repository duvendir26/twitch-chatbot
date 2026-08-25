# Duel system that will utilize stats (hp, armor, strength) to determine the outcome of a duel. Players can challenge each other to duels and wager coins on the outcome. The winner will receive the wagered coins and the loser will lose them. The duel system will also keep track of wins and losses for each player.

# If player dies in a duel they will lose their keks

# If a player avoids dueling for a certain amount of time, they will lose their keks as a penalty for not participating in duels. This will encourage players to engage in duels and keep the game active. (Make sure its not abused by players who are inactive for a long time and then come back to duel and win keks from other players). Need to check for last message time.

from config import COMMAND_PREFIX
from utils.users import get_user, load_users


async def cmd_duel(username, reply, args=None):
    print(f"@{username} requested duel command with args: {args}")
    
    args = args or []
    
    if len(args) < 2:
        await reply(
            f"@{username} Usage: "
            f"{COMMAND_PREFIX}duel <opponent> <amount>"
        )
        return
    
    if args[0].lower() == username.lower():
        await reply(
            f"@{username} You cannot duel yourself KEKScreen"
        )
        return
    
    users = load_users()
    if args[0].lower() not in [user["username"].lower() for user in users]:
        await reply(
            f"@{username} Opponent not found KEKScreen"
        )
        return