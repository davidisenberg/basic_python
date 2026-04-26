import os
import requests
import pandas as pd

#Documentation - https://documenter.getpostman.com/view/664302/S1ENwy59#674e81c1-6a0c-4836-8a7e-6ea1fe8e6677

def _load_api_key():
    key = os.environ.get('EBIRD_API_KEY')
    if key:
        return key
    try:
        from .ebird_api_key import get_api_key
        return get_api_key()
    except ImportError:
        raise RuntimeError("Set the EBIRD_API_KEY environment variable")

api_token = _load_api_key()

def get_ebird_taxonomy():
    url =  'https://api.ebird.org/v2/ref/taxonomy/ebird?fmt=json'
    headers = {
    "X-eBirdApiToken": api_token
    }

    # Send GET request
    response = requests.get(url, headers=headers)
    return process_response(response)


def get_ebird_hotspots(lat, long):
    print("ebird hotspots")
    url = 'https://api.ebird.org/v2/ref/hotspot/geo?fmt=json&dist=500&back=14&lat=' + str(lat) + '&lng=' + str(long) 
    headers = {
    "X-eBirdApiToken": api_token
    }

    # Send GET request
    response = requests.get(url, headers=headers)
    return process_response(response)

def get_recent_obs(lat, long):
    """Return DataFrame of recent observations near a point (last 14 days, 0.5km radius)."""
    url = 'https://api.ebird.org/v2/data/obs/geo/recent?back=14&dist=.5&lat=' + str(lat) + '&lng=' + str(long)
    headers = {"X-eBirdApiToken": api_token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return pd.json_normalize(response.json())
    return pd.DataFrame()


def get_checklist_stats(loc_id, back=14):
    """Return (num_checklists, num_contributors) for a hotspot over the last N days."""
    import datetime
    url = f'https://api.ebird.org/v2/product/lists/{loc_id}?maxResults=200'
    headers = {"X-eBirdApiToken": api_token}
    response = requests.get(url, headers=headers)
    if response.status_code != 200 or not response.json():
        return 0, 0
    df = pd.json_normalize(response.json())
    cutoff = datetime.date.today() - datetime.timedelta(days=back)
    if 'obsDt' in df.columns:
        df['_date'] = pd.to_datetime(df['obsDt'], format='mixed', dayfirst=False).dt.date
        df = df[df['_date'] >= cutoff]
    num_checklists = len(df)
    # eBird may return userDisplayName or firstName/lastName
    if 'userDisplayName' in df.columns:
        num_contributors = df['userDisplayName'].nunique()
    elif 'firstName' in df.columns:
        df['_name'] = df['firstName'].fillna('') + df['lastName'].fillna('')
        num_contributors = df['_name'].nunique()
    else:
        num_contributors = 0
    return num_checklists, num_contributors

def get_indigo(lat, long):
    url =  'https://api.ebird.org/v2/data/obs/geo/recent/indbun?lat=' +str(lat) + '&lng=' + str(long) 
    headers = {
    "X-eBirdApiToken": api_token
    }

    # Send GET request
    response = requests.get(url, headers=headers)
    return process_response(response)

#get_subregion("US-NJ")  #US-NJ-017	
def get_subregion(region: str):

    url = 'https://api.ebird.org/v2/ref/region/list/subnational2/' + region
    headers = {
    "X-eBirdApiToken": api_token
    }

    # Send GET request
    response = requests.get(url, headers=headers)
    return process_response(response)

#get_obs("US-NJ-017")
def get_obs(lat, long):
    # Set API token and URL
    #url = 'https://api.ebird.org/v2/data/obs/' + region + '/recent'
    url = "https://api.ebird.org/v2/data/obs/geo/recent?lat=" + str(lat) + '&lng=' + str(long) + "&includeProvisional=true&dist=50&back=30"
    headers = {
    "X-eBirdApiToken": api_token
    }

    # Send GET request
    response = requests.get(url, headers=headers)
    return process_response(response)


def process_response(response):
    if response.status_code == 200:
        data = response.json()
        df = pd.json_normalize(data)
        return df
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


