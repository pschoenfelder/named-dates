import pytest

import datetime
from named_dates import is_named_date
from named_dates.named_dates import _named_dates


def test_named_date_aliases():
    mlk = datetime.date(2015, 1, 19)
    assert is_named_date(mlk, "Martin Luther King, Jr. Day")
    assert is_named_date(mlk, "Martin Luther King Jr. Day")
    assert is_named_date(mlk, "MLK Day")

    presidents = datetime.date(2015, 2, 16)
    assert is_named_date(presidents, "Washington's Birthday")
    assert is_named_date(presidents, "President's Day")


def test_no_duplicate_storage_for_aliases():
    assert _named_dates["Washington's Birthday"] is\
           _named_dates["President's Day"]
