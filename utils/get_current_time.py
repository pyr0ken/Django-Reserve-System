from pytz import timezone as pytz_timezone
from django.utils import timezone


def get_current_time():
    # Set the desired timezone
    desired_timezone = pytz_timezone('Asia/Tehran')

    # Get the current time in the desired timezone
    current_time = timezone.now().astimezone(desired_timezone)

    return current_time
