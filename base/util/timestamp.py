import datetime
import time


# TODO: Test and consider about time zone issue.

def datetime_to_timestamp(dt):
    return time.mktime(dt.timetuple())


def timestamp_to_datetime(ts):
    return datetime.datetime.fromtimestamp(ts)
