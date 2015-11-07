import pytest

from datetime import date

import named_dates
from named_dates import NamedDate


def test_hard_NamedDate():
    hard_date = NamedDate("SpecialDate", 9, 25)
    assert hard_date.falls_on(date(1937, 9, 25))
    assert hard_date.falls_on(date(2014, 9, 25))
    assert not hard_date.falls_on(date(2014, 12, 17)


def test_soft_NamedDate():
    soft_date = NamedDate("MyDate", 11, 3, nth=4, aliases=['MyDate2'])
    assert set(soft_date.names) == set(["MyDate", "MyDate2"])
    assert soft_date.falls_on(date(2015, 11, 26))
    assert soft_date.falls_on(date(2016, 11, 24))
    assert soft_date.falls_on(date(2017, 11, 23))
    assert not soft_date.falls_on(date(2014, 11, 26))
    assert not soft_date.falls_on(date(2015, 11, 25))
    assert not soft_date.falls_on(date(2015, 11, 27))


def test_soft_from_end_NamedDate():
    my_date = NamedDate("Memorial Day", 5, 0, nth=1, from_end=True)
    assert my_date.falls_on(date(2015, 5, 25))
    assert my_date.falls_on(date(2016, 5, 30))
    assert my_date.falls_on(date(1971, 5, 31))


def test_custom_function_NamedDate():
    my_date = NamedDate("MyDate", custom_func=lambda x: x.day == 25)
    assert my_date.falls_on(date(2015, 10, 25))
    assert my_date.falls_on(date(1999, 12, 25))
    assert not my_date.falls_on(date(2015, 10, 26))

    def custom_date_function(the_date):
        return the_date.month == 7

    my_date = NamedDate("MyDate", custom_func=custom_date_function)
    assert my_date.falls_on(date(2015, 7, 25))
    assert my_date.falls_on(date(1999, 7, 25))
    assert not my_date.falls_on(date(2015, 10, 25))


def test_bad_creation_specifications():
    with pytest.raises(named_dates.MissingArgumentsError):
        NamedDate("Nope")

    with pytest.raises(named_dates.MissingArgumentsError):
        NamedDate("Nope", 1)

    with pytest.raises(named_dates.MissingArgumentsError):
        NamedDate("Nope", day=1)

    with pytest.raises(TypeError):
        NamedDate("Nope", bad_kwarg=1)
