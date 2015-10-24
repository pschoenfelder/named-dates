import pytest

from datetime import date
from named_dates import register_named_date, make_named_date_group,\
    in_named_date_group  #, add_named_date_to_group


def test_named_date_groups():
    register_named_date("DateA", 11, 3, nth=4)
    register_named_date("DateB", 11, 28)
    register_named_date("DateC", 9, 25)

    make_named_date_group("GroupC", ["DateC"])
    make_named_date_group("GroupAB", ["DateA", "DateB"])
    # assert set(get_named_dates_in_group("GroupB")) == {"DateA", "DateB"}

    assert in_named_date_group(date(2015, 11, 26), "GroupAB")
    assert in_named_date_group(date(2015, 11, 28), "GroupAB")
    assert not in_named_date_group(date(2015, 9, 25), "GroupAB")
    assert in_named_date_group(date(1937, 9, 25), "GroupC")

    # add_named_date_to_group("DateA", "GroupC")
    # assert set(get_named_dates_in_group("GroupC")) == {"DateC", "DateA"}
    #
    # assert in_named_date_group(date(2015, 11, 26), "GroupC")




