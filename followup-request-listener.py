import os
import time

from datetime import datetime, timedelta
from time import sleep

from dotenv import load_dotenv
from api import SkyPortal
from utils import is_night, timezone, get_next_sunset, get_next_sunrise

load_dotenv()

skyportal_url = os.getenv("SKYPORTAL_URL")
skyportal_api_key = os.getenv("SKYPORTAL_API_KEY")
allocation_id = os.getenv("ALLOCATION_ID")


def retrieve_followup_requests(payload):
    """Function to retrieve new follow-up requests from skyportal"""
    status, data = skyportal.get_followup_requests(payload)
    if status != 200 or 'data' not in data:
        print(f"Error fetching follow-up requests: {data}")
        return None
    return data['data']['followup_requests']


if __name__ == '__main__':
    skyportal = SkyPortal(instance=skyportal_url, token=skyportal_api_key)
    last_refresh_date=datetime.utcnow() - timedelta(days=5) # update initial lookback time here
    payload = {
        "allocationID": allocation_id,
        "startDate": last_refresh_date,
        "status": "submitted"
    }
    while True:
        now = datetime.now(timezone)
        if not is_night(now):
            next_sunset = get_next_sunset(now)
            wait_time = (next_sunset - now).total_seconds()
            print(f"Waiting until next sunset at {next_sunset} ({wait_time} seconds)")
            time.sleep(wait_time)
            continue

        rise_time = get_next_sunrise(now)
        print(f"Listening for follow-up requests until sunrise at {rise_time}")
        while datetime.now(timezone) < rise_time:
            last_refresh_date=datetime.utcnow() # update last refresh time
            followup_requests=retrieve_followup_requests(payload)
            if followup_requests is None:
                sleep(30)
                continue

            #TODO: process follow-up requests here

            payload["startDate"] = last_refresh_date # update start date for next query
            sleep(20)