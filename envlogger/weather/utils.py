"""
Helper functions
"""
from datetime import datetime

def unix_to_python(timestamp):
    """
    Convert unix timestamp to python datetime
    """
    # Not sure how correct this is to do here, but return 'null' if the timestamp provided is 0
    if int(timestamp) == 0:
        return None
    else:
        return datetime.utcfromtimestamp(float(timestamp))

