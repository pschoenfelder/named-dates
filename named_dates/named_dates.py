import calendar
import datetime

_named_dates = {}
_named_date_groups = {}

class NamedDateError(Exception):
    pass


class NoNthWeekdayError(NamedDateError):
    pass


class MissingArgumentsError(NamedDateError):
    pass


def day_of_nth_weekday(year, month, weekday, nth=1, from_end=False):
    """Determine the day of the month on which the ``nth`` time that ``weekday``
     occurs in the ``month`` of ``year``.

    :param year: Year
    :param month: Month
    :param weekday: Integer representing the day of week (0-6, Monday through
     Sunday).
    :param nth: The number occurrence of ``weekday`` in ``month`` of ``year``.
    :param from_end: If True, then ``nth`` looks backwards from the
     end of ``month``of ``year``.
    :return: An integer day of the month.
    :raises NoNthWeekdayException: If no nth weekday exists for this month
     and year.
    """
    days_in_month = calendar.monthrange(year, month)[1]
    reference_day = 1 if not from_end else days_in_month
    reference_weekday = datetime.date(year, month, reference_day).weekday()

    nth_offset = 7 * (nth-1)
    if ((not from_end and weekday < reference_weekday) or
            (from_end and weekday > reference_weekday)):
        nth_offset += 7

    if from_end:
        nth_offset = -nth_offset

    day = reference_day + nth_offset + weekday - reference_weekday
    if nth < 1 or not (1 <= day <= days_in_month):
        raise NoNthWeekdayError()

    return day


def register_named_date(name, month=None, day=None,
                        nth=None, from_end=False, custom_func=None):
    """Register a named date.

    :param name: The name of the date. Must be unique within all named dates.
    :param month: Month.
    :param day: If nth is None, represents a specific day in ``month``.
     Otherwise, represents a weekday (0-6, Monday-Sunday).
    :param nth: The number occurrence of ``day`` (as a weekday) in ``month``
     of ``year``.
    :param from_end: Logical. If True, then ``nth`` looks backwards from the
     end of ``month``of ``year``.
    :param custom_func: A user defined function for determining whether an
     input date is a named date. If provided, all other arguments except name
     are ignored. The function should take the form::
        def my_func(date):
            return True if date is the named date else False
    """
    global _named_dates

    if not custom_func:
        if not (month and day):
            raise MissingArgumentsError(
                "month and day, or custom_func, must be specified to " +
                "register a date. ")
        if nth:
            def is_date(date):
                nth_weekday = day_of_nth_weekday(date.year, date.month,
                                                 day, nth, from_end)
                return date.month == month and date.day == nth_weekday
        else:
            def is_date(date):
                return date.month == month and date.day == day
    else:
        is_date = custom_func

    _named_dates[name] = is_date


def is_named_date(date, name):
    """Check if ``date`` is represented by ``name``."""
    is_date_func = _named_dates.get(name, None)
    return is_date_func(date) if is_date_func else False


def clear_named_dates():
    _named_dates.clear()


def make_named_date_set(group, date_names=None):
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



