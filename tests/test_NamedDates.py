import pytest

from datetime import date
import named_dates
from named_dates import NamedDate, NamedDates, NamedDatesKeyError


def test_NamedDates():
    my_date = NamedDate("MyDate", 1, 1)

    my_dates = NamedDates()
    my_dates.add(my_date)
    my_dates.add(NamedDate("Martin Luther King, Jr. Day", 1, 0, nth=3,
                           aliases=["Martin Luther King Jr. Day", "MLK Day"]))

    assert my_dates.observes(date(2015, 1, 19))
    assert my_dates.observes(date(2015, 1, 1))
    assert my_dates.observes(date(2005, 1, 1))

    presidents_day = date(2015, 2, 16)
    assert not my_dates.observes(presidents_day)
    with pytest.raises(named_dates.NamedDatesKeyError):
        my_dates["Washington's Birthday"]

    my_dates.add(NamedDate("Washington's Birthday", 2, 0, nth=3,
                           aliases=["President's Day"]))
    assert my_dates.observes(presidents_day)

    assert my_dates["Washington's Birthday"]
    assert my_dates["President's Day"].falls_on(presidents_day)

    assert set(my_dates.names) == {"MyDate",
                                   "Washington's Birthday",
                                   "President's Day",
                                   "Martin Luther King, Jr. Day",
                                   "Martin Luther King Jr. Day",
                                   "MLK Day"}


def test_NamedDatesErrors():
    my_date = NamedDate("MyDate", 1, 1)
    with pytest.raises(NamedDatesKeyError):
        NamedDates([my_date, my_date])

    my_dates = NamedDates([my_date])
    with pytest.raises(NamedDatesKeyError):
        my_dates.add(my_date)

    with pytest.raises(NamedDatesKeyError):
        my_dates["uhoh"]

# def test_NamedDate():
#     mlk = NamedDate("Martin Luther King, Jr. Day", 1, 0, nth=3,
#                     aliases=["Martin Luther King Jr. Day", "MLK Day"])
#
#     real_date = date(2015, 1, 1)
#     assert real_date == my_date
#     assert my_date.for_year(2015) == real_date
#     assert real_date == my_date.for_year(2015)
#     assert my_date.is_same(real_date)
#     assert is_named_date(real_date, my_date)
#
#
#
#     my_date = date(2015, 1, 1)
#     assert my_date in NYSEHolidays
#     assert my_date == NYSEHolidays["Thanksgiving"]
#
#     assert NYSEHolidays["Thanksgiving"].falls_on(my_date)
#     assert NYSEHolidays.observes(my_date)


