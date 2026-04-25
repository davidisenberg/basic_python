import requests
import time

ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6Ijg4MTg3MTJjMjEzYzQxOGVhNzYxOTQxMjhlNzNlMDhkIiwiaCI6Im11cm11cjY0In0="
ORS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"


def get_ride_time(lat1, lon1, lat2, lon2) -> int:
    """Return driving duration in seconds between two points. Returns None on failure."""
    time.sleep(1.5)  # ORS rate limit: 40 req/min on free tier
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json",
    }
    body = {
        "coordinates": [[float(lon1), float(lat1)], [float(lon2), float(lat2)]],
        "radiuses": [-1, -1],
    }
    try:
        response = requests.post(ORS_URL, json=body, headers=headers, timeout=10)
        if response.status_code == 200:
            duration = response.json()["routes"][0]["summary"]["duration"]
            return int(duration)
        else:
            print(f"ORS error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"ORS exception: {e}")
        return None
