import calendar
import datetime

_named_dates = {}


class NoNthWeekdayException(Exception):
    pass


def day_of_nth_weekday(year, month, weekday, nth=1):
    """Determine the day of the month on which the ``nth`` time that ``weekday``
     occurs in the ``month`` of ``year``.

    :param year: Year
    :param month: Month
    :param weekday: Integer representing the day of week (0-6, Monday through
     Sunday).
    :param nth: The number occurrence of ``weekday`` in ``month`` of ``year``.
    :return: An integer day of the month.
    :raises NoNthWeekdayException: If no nth weekday exists for this month
     and year.
    """
    first_of_month_weekday = datetime.date(year, month, 1).weekday()
    nth_offset = 7 * (nth-1)
    if weekday < first_of_month_weekday:
        nth_offset += 7

    day = (weekday - first_of_month_weekday + 1) + nth_offset
    if nth < 1 or day > calendar.monthrange(year, month)[1]:
        raise NoNthWeekdayException()

    return day


def create_named_date(name, month, day, nth=None):
    """Register a named date.

    :param name: The name of the date. Must be unique within all named dates.
    :param month: Month.
    :param day: If nth is None, represents a specific day in ``month``.
     Otherwise, represents a weekday (0-6, Monday-Sunday).
    :param nth: The number occurrence of ``day`` (as a weekday) in ``month``
     of ``year``.
    """
    global _named_dates

    if nth:
        def is_date(date):
            nth_weekday = day_of_nth_weekday(date.year, date.month, day, nth)
            return date.month == month and date.day == nth_weekday
    else:
        def is_date(date):
            return date.month == month and date.day == day

    _named_dates[name] = is_date


def is_named_date(date, name):
    """Check if ``date`` is represented by ``name``."""
    is_date_func = _named_dates.get(name, None)
    return is_date_func(date) if is_date_func else False


def clear_named_dates():
    _named_dates.clear()
