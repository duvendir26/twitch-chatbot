def format_duration(seconds):
    """Format seconds as e.g. '1h 2m 3s', omitting zero-valued leading units."""
    seconds = max(0, int(seconds))
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)

    return (
        f"{str(hours) + 'h ' if hours else ''}"
        f"{str(minutes) + 'm ' if minutes else ''}"
        f"{secs}s"
    )
