"""Unit test thuần: không cần database."""
from datetime import datetime, timedelta, timezone

import pytest

from app.services.errors import ServiceError, parse_date, parse_int
from app.services.schedule_utils import VN_TZ, schedule_label, slot_key, to_local


def test_to_local_none():
    assert to_local(None) is None


def test_to_local_converts_utc_to_vietnam_time():
    utc = datetime(2026, 9, 7, 1, 0, tzinfo=timezone.utc)
    assert to_local(utc).hour == 8


def test_to_local_keeps_naive_datetime():
    naive = datetime(2026, 9, 7, 8, 0)
    assert to_local(naive) == naive


def test_schedule_label():
    assert schedule_label(datetime(2026, 9, 7, 8, 0, tzinfo=VN_TZ)) == "Monday · 08:00"
    assert schedule_label(None) == ""


def test_slot_key_same_weekday_and_time_in_different_weeks_is_equal():
    week1 = datetime(2026, 9, 7, 8, 0, tzinfo=VN_TZ)
    week2 = week1 + timedelta(days=7)
    assert slot_key(week1) == slot_key(week2)


def test_slot_key_differs_when_time_differs():
    a = datetime(2026, 9, 7, 8, 0, tzinfo=VN_TZ)
    assert slot_key(a) != slot_key(a.replace(hour=9))


def test_parse_int_ok():
    assert parse_int(" 5 ", "Credits", 1, 10) == 5


@pytest.mark.parametrize("value", ["abc", "", None, "1.5"])
def test_parse_int_rejects_non_integer(value):
    with pytest.raises(ServiceError, match="Credits must be a whole number"):
        parse_int(value, "Credits", 1, 10)


@pytest.mark.parametrize("value", ["0", "11"])
def test_parse_int_rejects_out_of_range(value):
    with pytest.raises(ServiceError, match="between 1 and 10"):
        parse_int(value, "Credits", 1, 10)


def test_parse_date_ok():
    assert parse_date("2026-09-01", "Start").isoformat() == "2026-09-01"


@pytest.mark.parametrize("value", ["01/09/2026", "", None, "2026-13-40"])
def test_parse_date_rejects_invalid(value):
    with pytest.raises(ServiceError, match="Start is not a valid date"):
        parse_date(value, "Start")
