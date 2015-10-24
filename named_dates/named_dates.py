import calendar
import datetime
from dateutil.easter import easter

_named_dates = {}
_named_date_groups = {}

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


def register_named_date(name, month, day, nth=None):
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


def make_named_date_group(group, date_names=None):
    """

    :param group: The group name
    :param date_names: A list of named date names to add
    """
    global _named_date_groups
    _named_date_groups[group] = list(date_names) if date_names else []


def in_named_date_set(date, group):
    for date_name in _named_date_groups.get(group, []):
        if _named_dates[date_name](date):
            return True

    return False


# def add_named_dates_to_group(named_dates, group):
#     global _named_date_groups
#     named_dates = list(named_dates)
#
#     named_dates.extend(_named_date_groups.get(group, []))
#     _named_date_groups[group] = named_dates


# def get_named_dates_in_group(group):
#     return _named_date_groups.get(group, [])

def is_easter(date):
    # Defaults to western Easter.
    return date == easter(date.year)


_named_dates["Easter Sunday"] = is_easter


