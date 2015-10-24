import pytest

from datetime import date
from named_dates import is_named_date
import named_dates.named_dates as nd

def test_easter():
    assert nd._named_dates["Easter Sunday"]
    assert is_named_date(date(1848, 4, 23), "Easter Sunday")
    assert is_named_date(date(1905, 4, 23), "Easter Sunday")
    assert is_named_date(date(1943, 4, 25), "Easter Sunday")
    assert is_named_date(date(2011, 4, 24), "Easter Sunday")
    assert is_named_date(date(2163, 4, 24), "Easter Sunday")
    assert is_named_date(date(2383, 4, 24), "Easter Sunday")

