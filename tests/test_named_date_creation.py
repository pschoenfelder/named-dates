import pytest

from datetime import date
from named_dates import create_named_date, is_named_date
from named_dates.named_dates import clear_named_dates


def test_named_date_creation():
    create_named_date("MyDate", 11, 3, nth=4)
    assert is_named_date(date(2015, 11, 26), "MyDate")
    assert is_named_date(date(2016, 11, 24), "MyDate")
    assert is_named_date(date(2017, 11, 23), "MyDate")
    assert not is_named_date(date(2014, 11, 26), "MyDate")
    assert not is_named_date(date(2015, 11, 25), "MyDate")
    assert not is_named_date(date(2015, 11, 27), "MyDate")

    create_named_date("MyDateHard", 11, 26)
    assert is_named_date(date(2016, 11, 26), "MyDateHard")
    assert is_named_date(date(2015, 11, 26), "MyDateHard")
    assert is_named_date(date(2014, 11, 26), "MyDateHard")
    assert not is_named_date(date(2015, 11, 25), "MyDateHard")
    assert not is_named_date(date(2016, 11, 24), "MyDateHard")


    create_named_date("SpecialDate", 9, 25)
    assert is_named_date(date(1939, 9, 25), "SpecialDate")
    assert is_named_date(date(2014, 9, 25), "SpecialDate")
    assert not is_named_date(date(2014, 12, 17), "SpecialDate")


def test_named_dates_persist():
    # Test order matters.
    # Depends on test_named_date_creation having already run.
    assert is_named_date(date(2015, 11, 26), "MyDate")


def test_non_existing_named_date():
    clear_named_dates()
    assert not is_named_date(date(2000, 1, 1), "NotANamedDate")
