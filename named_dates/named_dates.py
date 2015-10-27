import calendar
import datetime

from dateutil.easter import easter

_named_dates = {}
_named_date_sets = {}


class NamedDateError(Exception):
    pass


class NoNthWeekdayError(NamedDateError):
    pass


class MissingArgumentsError(NamedDateError):
    pass


class NamedDateKeyError(NamedDateError):
    pass


class NamedDateSetKeyError(NamedDateError):
    pass


def day_of_nth_weekday(year, month, weekday, **kwargs):
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
    nth = kwargs.pop('nth', 1)
    from_end = kwargs.pop('from_end', False)
    if kwargs:
        raise TypeError("Unexpected **kwargs: %r" % kwargs)

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


def register_named_date(name, month=None, day=None, **kwargs):
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
    :param aliases: A list of alternative names this date can be referenced by
    """
    global _named_dates

    nth = kwargs.pop('nth', None)
    from_end = kwargs.pop('from_end', None)
    custom_func = kwargs.pop('custom_func', None)
    aliases = kwargs.pop('aliases', None)
    if kwargs:
        raise TypeError("Unexpected **kwargs: %r" % kwargs)

    if not custom_func:
        if day is None or month is None:
            raise MissingArgumentsError(
                "month and day, or custom_func, must be specified to " +
                "register a date. ")
        if nth:
            def is_date(date):
                nth_weekday = day_of_nth_weekday(date.year, date.month, day,
                                                 nth=nth, from_end=from_end)
                return date.month == month and date.day == nth_weekday
        else:
            def is_date(date):
                return date.month == month and date.day == day
    else:
        is_date = custom_func

    if aliases:
        for alias in aliases:
            _named_dates[alias] = is_date

    _named_dates[name] = is_date


def is_named_date(date, name):
    """Check if ``date`` is represented by ``name``."""
    try:
        is_date_func = _named_dates[name]
    except KeyError:
        raise NamedDateKeyError(name)

    return is_date_func(date)


def clear_named_dates():
    _named_dates.clear()


def make_named_date_set(set_name, date_names):
    """Create a set of named dates.

    :param set_name: The group name.
    :param date_names: A single string or set or list of named date
     names to add.
    """
    global _named_date_sets

    date_names = set(date_names)

    # Validate that each listed date exists.
    try:
        for name in date_names:
            _ = _named_dates[name]
    except KeyError as e:
        raise NamedDateKeyError(
            'Cannot make named date set from non-existing named date "' +
            str(e) + '".')

    _named_date_sets[set_name] = date_names


def in_named_date_set(date, set_name):
    try:
        date_names = _named_date_sets[set_name]
    except KeyError:
        raise NamedDateSetKeyError(set_name)

    for date_name in date_names:
        if _named_dates[date_name](date):
            return True

    return False


def get_named_dates_in_set(set_name):
    try:
        names = _named_date_sets[set_name]
    except KeyError:
        raise NamedDateSetKeyError(set_name)

    return names

# Base named dates that come with the import
register_named_date("New Years Day", 1, 1, aliases=["New Years"])
register_named_date("Martin Luther King, Jr. Day", 1, 0, nth=3,
                    aliases=["Martin Luther King Jr. Day", "MLK Day"])
register_named_date("Washington's Birthday", 2, 0, nth=3,
                    aliases=["President's Day"])


def is_good_friday(date):
    # Defaults to western Easter.
    return date == easter(date.year) - datetime.timedelta(days=2)

register_named_date("Good Friday", custom_func=is_good_friday)
register_named_date("Memorial Day", 5, 0, nth=1, from_end=True)
register_named_date("Independence Day", 7, 4)
register_named_date("Labor Day", 9, 0, nth=1)
register_named_date("Thanksgiving Day", 11, 3, nth=4, aliases=["Thanksgiving"])
register_named_date("Christmas Day", 12, 25, aliases=["Christmas"])

# The extra half day holidays on Thanksgiving and Christmas are not included.
make_named_date_set("NYSEHolidays", ["New Years Day",
                                     "Martin Luther King, Jr. Day",
                                     "Washington's Birthday",
                                     "President's Day",
                                     "Good Friday",
                                     "Memorial Day",
                                     "Independence Day",
                                     "Labor Day",
                                     "Thanksgiving Day",
                                     "Christmas Day"])
