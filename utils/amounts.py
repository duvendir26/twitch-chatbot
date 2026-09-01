def parse_int_amount(arg):
    """Parse `arg` as an int, returning None if invalid."""
    try:
        return int(arg)
    except ValueError:
        return None


async def parse_positive_amount(
    reply,
    viewer,
    arg,
    *,
    allow_all=False,
    all_amount=0,
    cap=None,
    invalid_message=None,
    zero_message=None,
):
    """
    Parse `arg` into a positive int amount, optionally supporting 'all'/'full'.
    Replies and returns None if the amount is invalid or non-positive.
    Otherwise returns the amount, capped at `cap` if provided.
    """
    arg = (arg or "").lower()

    if allow_all and arg in ("all", "full"):
        amount = all_amount() if callable(all_amount) else all_amount
    else:
        amount = parse_int_amount(arg)

        if amount is None:
            if invalid_message:
                await reply(invalid_message)
            else:
                suffix = " or 'all'" if allow_all else ""
                await reply(f"@{viewer} Enter a valid number{suffix} KEKP")
            return None

    if amount <= 0:
        await reply(
            zero_message or f"@{viewer} Amount must be greater than 0 KEKP"
        )
        return None

    if cap is not None:
        amount = min(amount, cap)

    return amount
