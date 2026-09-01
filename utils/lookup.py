def find_by_name(items, name, key="name"):
    """Case-insensitive lookup of a dict by its `key` field in a list of dicts."""
    return next(
        (item for item in items if item[key].lower() == name.lower()),
        None
    )
