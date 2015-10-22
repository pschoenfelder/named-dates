import calendar
from datetime import date


class NoNthWeekdayException(Exception):
    pass


def day_of_nth_weekday(year, month, weekday, nth=1):
    """Determine the day of the month on which the ``nth`` time that ``weekday``
     occurs in the ``month`` of ``year``.

    :param year: Year
    :param month: Month
    :param weekday: Integer representing the day of week (0-6, Monday through
     Sunday).
    :param nth: The number occurrence of ``weekday``
    :return: An integer day of the month.
    :raises NoNthWeekdayException: If no nth weekday exists for this month
     and year.
    """
    first_of_month_weekday = date(year, month, 1).weekday()
    nth_offset = 7 * (nth-1)
    if weekday < first_of_month_weekday:
        nth_offset += 7

    day = (weekday - first_of_month_weekday + 1) + nth_offset
    if nth < 1 or day > calendar.monthrange(year, month)[1]:
        raise NoNthWeekdayException()

    return day
