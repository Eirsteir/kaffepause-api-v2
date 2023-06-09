from datetime import datetime, timedelta

import pytz

from kaffepause.core.config import settings


def now():
    return time_from_now()


def fifteen_minutes_from_now():
    return time_from_now(minutes=15)


def three_hours_from_now():
    return time_from_now(hours=3)


def format_kicker_message(time):
    time_str = format_time_from_now(time)
    return "Om %(time)s" % {"time": time_str}


def format_time_from_now(
    target_time,
) -> str:  # TODO: håndter enkelte timer (time) og minutter (minutt)
    # Calculate the difference between the target time and the current time
    time_diff = target_time - now()
    # Extract the number of hours and minutes from the time difference
    hours = int(time_diff.total_seconds() // 3600)
    minutes = int((time_diff.total_seconds() % 3600) // 60)
    # Format the result based on the number of hours and minutes
    if hours > 0:
        result = "%(hours)d timer og %(minutes)d minutter" % {
            "hours": hours,
            "minutes": minutes,
        }
    else:
        result = "%(minutes)d minutter" % {"minutes": minutes}

    return result


def time_from_now(hours=0, minutes=0):
    """
    Returns the time from now.
    If now plus given time is in the past, it wraps around to the next day.
    """
    # Must use timezone aware datetime
    # becuase of neomodels implementation of DateTimeField
    now = datetime.now(pytz.utc)
    start = now + timedelta(hours=hours, minutes=minutes)
    return start if start >= now else start + timedelta(days=1)


def localize_datetime(dt, tz: str = settings.TIME_ZONE) -> datetime:
    """
    Convert a datetime object to a timezone-aware
    datetime object in the specified time zone.
    """
    target_timezone = pytz.timezone(tz)

    # Make the datetime object timezone-aware
    dt_aware = dt.replace(tzinfo=target_timezone)

    # Convert to the target time zone
    localized_dt = dt_aware.astimezone(target_timezone)

    return localized_dt
