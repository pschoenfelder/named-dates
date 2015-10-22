import pytest

from named_dates.named_dates import\
    day_of_nth_weekday, NoNthWeekdayException


# For reference throughout these tests, October 1, 2015 is
# a Thursday (weekday = 3).
def test_weekday_equals_first_of_month():
    # Tests that day_of_nth_weekday works when the requested weekday is the
    # first weekday is the month.
    assert day_of_nth_weekday(2015, 10, 3, nth=1) == 1
    assert day_of_nth_weekday(2015, 10, 3, nth=2) == 8
    assert day_of_nth_weekday(2015, 10, 3, nth=3) == 15
    assert day_of_nth_weekday(2015, 10, 3, nth=4) == 22
    assert day_of_nth_weekday(2015, 10, 3, nth=5) == 29
    with pytest.raises(NoNthWeekdayException):
        day_of_nth_weekday(2015, 10, 3, nth=0)
    with pytest.raises(NoNthWeekdayException):
        day_of_nth_weekday(2015, 10, 3, nth=6)


def test_weekday_greater_than_first_of_month():
    # Tests that day_of_nth_weekday works when the requested weekday is
    # greater than the first weekday of the month.
    assert day_of_nth_weekday(2015, 10, 5, nth=1) == 3
    assert day_of_nth_weekday(2015, 10, 5, nth=2) == 10
    assert day_of_nth_weekday(2015, 10, 5, nth=5) == 31
    with pytest.raises(NoNthWeekdayException):
        day_of_nth_weekday(2015, 10, 5, nth=6)


def test_weekday_less_than_first_of_month():
    # Tests that day_of_nth_weekday works when the requested weekday is
    # less than the first weekday of the month.
    assert day_of_nth_weekday(2015, 10, 1, nth=1) == 6
    assert day_of_nth_weekday(2015, 10, 1, nth=2) == 13
    assert day_of_nth_weekday(2015, 10, 1, nth=3) == 20
    assert day_of_nth_weekday(2015, 10, 1, nth=4) == 27
    with pytest.raises(NoNthWeekdayException):
        day_of_nth_weekday(2015, 10, 1, nth=5)
