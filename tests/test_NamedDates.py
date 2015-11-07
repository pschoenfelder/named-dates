import pytest

from datetime import date
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
    with pytest.raises(NamedDatesKeyError):
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
