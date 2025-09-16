# Followup Request Listener

A simple Python service that listens for follow-up requests during the night and wait during the day.

## Setup
```bash
git clone https://github.com/antoine-le-calloch/followup-request-listener.git
cd followup-request-listener
pip install -r requirements.txt
cp .env.default .env
```

## Configuration
Edit the `.env` file to set your configuration:
- `SKYPORTAL_URL`: The URL of your SkyPortal instance.
- `SKYPORTAL_API_KEY`: Your SkyPortal API key.
- `ALLOCATION_ID`: The ID of the allocation where the follow-up requests will be created.
- `LATITUDE`: Your observatory's latitude.
- `LONGITUDE`: Your observatory's longitude.

## Running the Service
```bash
python followup_request_listener.py
```