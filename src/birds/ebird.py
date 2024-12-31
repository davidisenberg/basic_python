import requests
import pandas as pd
from ebird_api_key import get_api_key

#Documentation - https://documenter.getpostman.com/view/664302/S1ENwy59#674e81c1-6a0c-4836-8a7e-6ea1fe8e6677

# Set API token and URL
api_token = get_api_key()

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

def get_numspecies_last14(lat, long):
    url = 'https://api.ebird.org/v2/data/obs/geo/recent?back=14&dist=.5&lat=' + str(lat) + '&lng=' + str(long) 
    headers = {
    "X-eBirdApiToken": api_token
    }

     # Send GET request
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        local_species = response.json()
        local_species_df = pd.json_normalize(local_species)
        return len(local_species_df)
    
    return 0

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


