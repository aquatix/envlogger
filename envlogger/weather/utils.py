"""
Helper functions
"""
from datetime import datetime, timezone


def unix_to_python(timestamp, utc=True):
    """
    Convert unix timestamp to python datetime
    """
    # Not sure how correct this is to do here, but return 'null' if the timestamp provided is 0
    if int(timestamp) == 0:
        return None
    else:
        tz = None
        if utc:
            tz = timezone.utc
        return datetime.fromtimestamp(float(timestamp), tz)
