import calendar
import datetime


class NamedDateError(Exception):
    pass


class NoNthWeekdayError(NamedDateError):
    pass


class MissingArgumentsError(NamedDateError):
    pass


class NamedDatesKeyError(NamedDateError):
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


class NamedDate(object):
    """An object that encapsulates the logic of dates often referenced by name
    instead of date because the date on which it falls usually varies from
    year to year."""

    def __init__(self, name, month=None, day=None, **kwargs):
        """
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
        nth = kwargs.pop('nth', None)
        from_end = kwargs.pop('from_end', False)
        custom_func = kwargs.pop('custom_func', None)
        aliases = kwargs.pop('aliases', [])
        if kwargs:
            raise TypeError("Unexpected **kwargs: %r" % kwargs)

        if not custom_func:
            if (not month) or (day is None):  # Beware, day == 0 is valid
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

        self.__is_date = is_date
        self._names = [name] + list(aliases)

    def falls_on(self, date):
        """Does this named date occur on ``date``?"""
        return self.__is_date(date)

    @property
    def names(self):
        return self._names


class NamedDates(object):
    """An object to represent a set of NamedDates."""
    def __init__(self, named_dates=[]):
        self.__named_dates = {}
        for named_date in named_dates:
            for name in named_date.names:
                if self.__named_dates.get(name) is not None:
                    raise NamedDatesKeyError("Conflicting duplicate name '%s' found." % name)
                self.__named_dates[name] = named_date

    def __getitem__(self, name):
        try:
            return self.__named_dates[name]
        except KeyError:
            raise NamedDatesKeyError(name)

    def add(self, named_date):
        for name in named_date.names:
            if self.__named_dates.get(name) is not None:
                raise NamedDatesKeyError("Conflicting duplicate name '%s' found." % name)
            self.__named_dates[name] = named_date

    def observes(self, date):
        return any([nd.falls_on(date) for nd in self.__named_dates.values()])

    @property
    def names(self):
        return self.__named_dates.keys()
