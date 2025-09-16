import os
import time
import pytz

from datetime import datetime, timedelta
from astral import LocationInfo
from astral.sun import sun
from timezonefinder import TimezoneFinder
from dotenv import load_dotenv

load_dotenv()
# SkyPortal utilities
skyportal_url = os.getenv("SKYPORTAL_URL")
skyportal_api_key = os.getenv("SKYPORTAL_API_KEY")

# Position of the observatory
latitude = float(os.getenv("LATITUDE"))
longitude = float(os.getenv("LONGITUDE"))

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


def retrieve_followup_requests():
    """Function to retrieve new follow-up requests from skyportal"""
    print("Retrieving follow-up requests...")


if __name__ == '__main__':
    while True:
        now = datetime.now(timezone)
        if not is_night(now):
            next_sunset = get_next_sunset(now)
            wait_time = (next_sunset - now).total_seconds()
            print(f"Waiting until next sunset at {next_sunset} ({wait_time} seconds)")
            time.sleep(wait_time)
            continue

        print(f"Listening for follow-up requests...")
