XP_PER_LEVEL = 1000
MAX_LEVEL = 30
KEK_MULTIPLIER_PER_LEVEL = 0.05  # +5% keks earned per level, tune to taste


def get_level(xp):
    """Player level based on xp, capped at MAX_LEVEL."""
    return min(xp // XP_PER_LEVEL, MAX_LEVEL)


def get_kek_multiplier(level):
    """Kek reward multiplier for a given level (1.0 = no bonus)."""
    return 1 + level * KEK_MULTIPLIER_PER_LEVEL


def add_xp(user, amount):
    """Add xp to `user` in place, capping at the xp needed for MAX_LEVEL."""
    user["xp"] = min(user.get("xp", 0) + amount, XP_PER_LEVEL * MAX_LEVEL)


def apply_kek_multiplier(user, amount):
    """Scale a kek reward by `user`'s level-based multiplier, rounded to an int."""
    level = get_level(user.get("xp", 0))
    return round(amount * get_kek_multiplier(level))
