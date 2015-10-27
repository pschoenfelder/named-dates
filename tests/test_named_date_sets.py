import pytest

from datetime import date
from named_dates import register_named_date, make_named_date_set,\
    in_named_date_set, get_named_dates_in_set,\
    NamedDateKeyError, NamedDateSetKeyError
from named_dates.named_dates import clear_named_date_sets


def test_named_date_sets():
    register_named_date("DateA", 11, 3, nth=4)
    register_named_date("DateB", 11, 28)
    register_named_date("DateC", 9, 25)

    make_named_date_set("GroupC", ["DateC"])
    make_named_date_set("GroupAB", ["DateA", "DateB"])

    assert in_named_date_set(date(2015, 11, 26), "GroupAB")
    assert in_named_date_set(date(2015, 11, 28), "GroupAB")
    assert not in_named_date_set(date(2015, 9, 25), "GroupAB")
    assert in_named_date_set(date(1937, 9, 25), "GroupC")

    assert get_named_dates_in_set("GroupC") == {"DateC"}
    assert get_named_dates_in_set("GroupAB") == {"DateA", "DateB"}


def test_non_existing_set():
    with pytest.raises(NamedDateSetKeyError):
        in_named_date_set(date(2015, 1, 1), "NonExistingSet")

    with pytest.raises(NamedDateSetKeyError):
        get_named_dates_in_set("NonExistingSet")


def test_existing_set_with_non_existing_named_date():
    with pytest.raises(NamedDateKeyError):
        make_named_date_set("MyNewSet",
                            ["Thanksgiving",
                             "NonExistingDate"])


def test_clear_named_date_sets():
    assert len(get_named_dates_in_set("NYSEHolidays")) > 0
    clear_named_date_sets()
    with pytest.raises(NamedDateSetKeyError):
        get_named_dates_in_set("NYSEHolidays")

