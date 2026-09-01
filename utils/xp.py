XP_PER_LEVEL = 1000
MAX_LEVEL = 30
XP_PER_KEK = 10  # $convert rate: 10 xp -> 1 kek, one-way only


def get_level(xp):
    """Player level based on xp, capped at MAX_LEVEL. Starts at level 1 (0-999 xp)."""
    return min(xp // XP_PER_LEVEL + 1, MAX_LEVEL)


def get_kek_bonus(level):
    """Flat kek bonus per level: +1 at level 1, +2 at level 2, etc."""
    return level


def add_xp(user, amount):
    """Add xp to `user` in place, capping at the xp needed for MAX_LEVEL. Returns the amount actually gained."""
    before = user.get("xp", 0)
    user["xp"] = min(before + amount, XP_PER_LEVEL * MAX_LEVEL)
    return user["xp"] - before


def apply_kek_multiplier(user, amount):
    """Add level-based flat bonus keks to reward."""
    level = get_level(user.get("xp", 0))
    return amount + get_kek_bonus(level)


def get_xp_progress(xp):
    """Progress (current, needed) toward the next level; needed=0 once MAX_LEVEL is reached."""
    level = get_level(xp)
    if level >= MAX_LEVEL:
        return 0, 0

    return xp - (level - 1) * XP_PER_LEVEL, XP_PER_LEVEL

