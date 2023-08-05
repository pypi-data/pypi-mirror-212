from datetime import datetime, timedelta, timezone


def get_utc3():
    # Create a timezone object for UTC-3
    UTC3 = timezone(timedelta(hours=-3))

    # Get the current datetime with UTC timezone
    NOW_UTC = datetime.now(timezone.utc)

    # Convert the UTC datetime to UTC-3 timezone
    NOW_UTC3 = NOW_UTC.astimezone(UTC3)

    return NOW_UTC3


def get_str():
    NOW_UTC3 = get_utc3()
    DATETIME = NOW_UTC3.strftime("%Y-%m-%d %H:%M:%S")

    return DATETIME


def get_path():
    NOW_UTC3 = get_utc3()

    # Use the filename to store in S3
    NOW_STR = f"year={NOW_UTC3.strftime('%Y')}/month={NOW_UTC3.strftime('%m')}/day={NOW_UTC3.strftime('%d')}/hour={NOW_UTC3.strftime('%H')}/minute={NOW_UTC3.strftime('%M')}"

    return NOW_STR
