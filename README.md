# Named Dates (WIP)
[![Build Status](https://travis-ci.org/pschoenfelder/named-dates.svg?branch=master)](https://travis-ci.org/pschoenfelder/named-dates)
[![Coverage Status](https://coveralls.io/repos/pschoenfelder/named-dates/badge.svg?branch=master&service=github)](https://coveralls.io/github/pschoenfelder/named-dates?branch=master)

The goal of named dates is to provide a simple API to keep track of special dates and their associated logic. 

### Usage
Need to recognize the 4th Thursday in November?
```python
register_named_date("Thanksgiving Day", 11, 3, nth=4,
                    aliases=["Thanksgiving", "Turkey Day"])
...
if is_named_date(my_date, "Thanksgiving"):
    print "TURKEY DAYYYYY"
```

How about a date based on the end of the month? Say, the last Monday in May?
```python
register_named_date("Memorial Day", 5, 0, nth=1, from_end=True)
```

Something more complex? Define a custom function.
```python
def is_good_friday(date):
    # Defaults to western Easter.
    return date == easter(date.year) - datetime.timedelta(days=2)

register_named_date("Good Friday", custom_func=is_good_friday)
```

You can even group important dates into sets, find out which dates are in a set, and find out whether a date is in a set.
```python
make_named_date_set("MyFavoriteHolidays", ["Thanksgiving",
                                           "Christmas",
                                           "New Years"])
get_named_dates_in_set("MyFavoriteHolidays")
# ["Thanksgiving", "Christmas", "New Years"]

if in_named_date_set(date(2015, 12, 25), "MyFavoriteHolidays"):
    print "Oct 31"
```

