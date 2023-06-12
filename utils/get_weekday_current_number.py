"""
Django weekday -> Sunday is 1 and Saturday is 7
Datetime module weekday -> Monday is 0 and Sunday is 6
"""


def get_weekday_current_number(weekday_number: int) -> int:
    if weekday_number == 0:
        return 2
    elif weekday_number == 1:
        return 3
    elif weekday_number == 2:
        return 4
    elif weekday_number == 3:
        return 5
    elif weekday_number == 4:
        return 6
    elif weekday_number == 5:
        return 7
    elif weekday_number == 6:
        return 1
