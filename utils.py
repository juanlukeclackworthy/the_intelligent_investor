def safe_cast(val, to_type=float, default=None):
    """
    Safely cast a value to a given type.

    Args:
        val: The value to cast.
        to_type: The type to cast to (default is float).
        default: The value to return if casting fails.

    Returns:
        The casted value, or the default if casting fails.
    """
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default