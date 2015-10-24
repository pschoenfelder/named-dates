import pytest

from datetime import date
from named_dates import is_named_date

def test_good_friday():
    assert is_named_date(date(1848, 4, 21), "Good Friday")
    assert is_named_date(date(1905, 4, 21), "Good Friday")
    assert is_named_date(date(1943, 4, 23), "Good Friday")
    assert is_named_date(date(2011, 4, 22), "Good Friday")
    assert is_named_date(date(2163, 4, 22), "Good Friday")
    assert is_named_date(date(2383, 4, 22), "Good Friday")

