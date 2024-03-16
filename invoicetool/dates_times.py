from datetime import datetime, timezone


def ymdhms_now() -> str:
    """Return the current date and time as a string formatted as YYYYMMDD_HHMMSS"""
    return datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")


def today2ymd() -> str:
    """Return the current date as a string formatted as YYYY-MM-DD"""
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
