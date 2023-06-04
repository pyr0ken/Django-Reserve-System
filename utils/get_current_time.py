from pytz import timezone as pytz_timezone
from datetime import datetime


def get_current_time():
    # Set the desired timezone
    desired_timezone = pytz_timezone('Asia/Tehran')

    # Get the current time in the desired timezone
    current_time = datetime.now(tz=desired_timezone)

    return current_time
