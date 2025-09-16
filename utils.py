import os
import pytz

from datetime import timedelta
from astral import LocationInfo
from astral.sun import sun
from dotenv import load_dotenv
from timezonefinder import TimezoneFinder

load_dotenv()

latitude = os.getenv("LATITUDE")
longitude = os.getenv("LONGITUDE")
timezone_str = TimezoneFinder().timezone_at(lat=latitude, lng=longitude)
timezone = pytz.timezone(timezone_str)
observer = LocationInfo(latitude=latitude, longitude=longitude, timezone=timezone_str).observer

def get_sun(date):
    """Return sun information for the given date"""
    return sun(observer, date=date, tzinfo=timezone)


def is_night(date):
    """Return True if it's currently nighttime"""
    s = get_sun(date)
    return s["sunset"] <= date or date <= s["sunrise"]

def get_next_sunset(date):
    """Return the next sunset time"""
    s = get_sun(date)
    if date < s["sunset"]:
        return s["sunset"]
    else:
        s = get_sun(date + timedelta(days=1))
        return s["sunset"]

def get_next_sunrise(date):
    """Return the next sunrise time"""
    s = get_sun(date)
    if date < s["sunrise"]:
        return s["sunrise"]
    else:
        s = get_sun(date + timedelta(days=1))
        return s["sunrise"]