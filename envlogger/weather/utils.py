"""
Helper functions
"""
from datetime import datetime
from pytz import UTC

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
            tz = UTC
        return datetime.fromtimestamp(float(timestamp), tz)

