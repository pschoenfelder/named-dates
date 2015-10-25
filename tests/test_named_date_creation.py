import pytest

from datetime import date
from named_dates import register_named_date, is_named_date
from named_dates.named_dates import clear_named_dates,\
    NamedDateKeyError, MissingArgumentsError


def test_named_date_creation():
    register_named_date("MyDate", 11, 3, nth=4)
    assert is_named_date(date(2015, 11, 26), "MyDate")
    assert is_named_date(date(2016, 11, 24), "MyDate")
    assert is_named_date(date(2017, 11, 23), "MyDate")
    assert not is_named_date(date(2014, 11, 26), "MyDate")
    assert not is_named_date(date(2015, 11, 25), "MyDate")
    assert not is_named_date(date(2015, 11, 27), "MyDate")

    register_named_date("MyDateHard", 11, 26)
    assert is_named_date(date(2016, 11, 26), "MyDateHard")
    assert is_named_date(date(2015, 11, 26), "MyDateHard")
    assert is_named_date(date(2014, 11, 26), "MyDateHard")
    assert not is_named_date(date(2015, 11, 25), "MyDateHard")
    assert not is_named_date(date(2016, 11, 24), "MyDateHard")

    register_named_date("SpecialDate", 9, 25)
    assert is_named_date(date(1937, 9, 25), "SpecialDate")
    assert is_named_date(date(2014, 9, 25), "SpecialDate")
    assert not is_named_date(date(2014, 12, 17), "SpecialDate")


def test_named_dates_persist():
    # Test order matters.
    # Depends on test_named_date_creation having already run.
    assert is_named_date(date(2015, 11, 26), "MyDate")


def test_non_existing_named_date():
    clear_named_dates()  # Just to be sure nothing exists.
    with pytest.raises(NamedDateKeyError):
        is_named_date(date(2000, 1, 1), "NotANamedDate")


def test_creation_via_custom_function():
    register_named_date(
        "CustomDate",
        custom_func=lambda x: x.day == 25)
    assert is_named_date(date(2015, 10, 25), "CustomDate")
    assert is_named_date(date(1999, 12, 25), "CustomDate")
    assert not is_named_date(date(2015, 10, 26), "CustomDate")

    def custom_date_function(the_date):
        return the_date.month == 7

    register_named_date(
        "CustomDate2",
        custom_func=custom_date_function)
    assert is_named_date(date(2015, 7, 25), "CustomDate2")
    assert is_named_date(date(1999, 7, 25), "CustomDate2")
    assert not is_named_date(date(2015, 10, 25), "CustomDate2")


def test_missing_creation_specifications():
    with pytest.raises(MissingArgumentsError):
        register_named_date("Nope")

    with pytest.raises(MissingArgumentsError):
        register_named_date("Nope", 1)

    with pytest.raises(MissingArgumentsError):
        register_named_date("Nope", day=1)