import pandas as pd
from birds.ebird import get_ebird_taxonomy, get_ebird_hotspots, get_numspecies_last14
from birds.tb_db import create_table, does_exist, get_local_taxonomy, get_local_hotspots, does_hotspot_exist, append_table, get_optimized_hotspots, does_golden_exist, get_local_goldens, get_duration, set_duration
from geopy.distance import geodesic
from here.here import get_ride_time

def get_tb_taxonomy():

    if does_exist("taxonomy"):
        return get_local_taxonomy()
    else:
        df = get_ebird_taxonomy()
        create_table("taxonomy",df)
        return df
    
def calculate_distance(lat1, lon1, lat2, lon2):
    point1 = (lat1, lon1)
    point2 = (lat2, lon2)
    distance_miles = geodesic(point1, point2).miles
    return distance_miles    

def get_tb_hotspots(name: str, lat, long):

    if does_exist("hotspots"):
        print("hotspot table exists")        
        if does_hotspot_exist(name):
            print("hotspot name exists - returning it")             
            df = get_local_hotspots(name)
            return df
        
    print("getting ebird hotspots")                     
    df = get_ebird_hotspots(lat, long)
    if not 'subnational2Code' in df.columns:
        df['subnational2Code'] = ''
    df['loc_name'] = name
    df['distance_miles'] = df.apply(lambda row: calculate_distance(row['lat'], row['lng'], lat, long), axis=1)
    df['duration'] = 0
    df['rank'] = df['numSpeciesAllTime'] ** 3 / df['distance_miles']

    df = df[['locId',	'locName',	'countryCode',	'subnational1Code',	'subnational2Code',	'lat',	'lng',	'latestObsDt',	'numSpeciesAllTime',	'loc_name'	,'distance_miles',	'duration',	'rank']]

    columns = df.columns
    print(columns)

    print("appending to table")                     
    append_table("hotspots",df)
    
    print("returning")                     
    return df      


def get_ride_time_or_cached(name, lat1, long1, lat2, long2):
    print("get ride time or cached: " + name + " " + str(lat1) + " " + str(long1))
    duration = get_duration(name, lat1, long1)
    print("duration in cache is: " + str(duration))
    if duration == 0:
        print("getting duration from API")
        duration = get_ride_time(lat1, long1, lat2, long2)
        if duration is not None:
            print("duration from API is: " + str(duration))
            set_duration(name, lat1, long1, duration)
        else:
            duration = 5 * 60 * 60 #arbitrarily make it 5 hours
            print("duration is None")
            set_duration(name, lat1, long1, duration)
    
    return duration

def get_saved_tb_goldens(name: str, max_num):
    if does_golden_exist(name + str(max_num)): 
        df = get_local_goldens(name + str(max_num))
        df['duration2'] = round(df['duration'] / 60 / 60,1)
        df = df[['locName','numSpeciesAllTime','distance_miles','numSpeciesTwoWeeks','golden_rank','duration2']]
        df = df.sort_values(by='golden_rank', ascending=False)
        return df   
    else:
        print("Not saved")

def get_tb_goldens(name: str, lat, long, max_num):

    if does_golden_exist(name + str(max_num)): 
        df = get_local_goldens(name + str(max_num))
        df['duration2'] = round(df['duration'] / 60 / 60,1)
        df = df[['locName','numSpeciesAllTime','distance_miles','numSpeciesTwoWeeks','golden_rank','duration2']]
        df = df.sort_values(by='golden_rank', ascending=False)
        return df   

    print("getting tbhotspots")  
    get_tb_hotspots(name, lat, long)
    df = get_optimized_hotspots(name, max_num)
    df['loc_name'] = name + str(max_num)
    print("getting last two weeks species")
    df['numSpeciesTwoWeeks'] = df.apply(lambda row: get_numspecies_last14(row['lat'], row['lng']), axis=1)
    print("getting ride times") 
    df['duration'] = df.apply(lambda row: get_ride_time_or_cached(name, row['lat'], row['lng'], str(lat), str(long)), axis=1)
    df['golden_rank'] = df['numSpeciesTwoWeeks'] ** 3 / (df['duration']/60/3)
        
    print("appending to table")        
    append_table("goldens", df)  

    df['duration2'] = round(df['duration'] / 60 / 60,1)

    df = df[['locName','numSpeciesAllTime','distance_miles','numSpeciesTwoWeeks','golden_rank','duration2']]
    df = df.sort_values(by='golden_rank', ascending=False)
    return df

def get_updated_goldens(name: str, lat, long, max_num):

    df = get_tb_goldens(name, lat, long, max_num)
    df['numSpeciesTwoWeeks'] = df.apply(lambda row: get_numspecies_last14(row['lat'], row['lng'], str(lat), str(long)), axis=1)
    df['golden_rank'] = df['numSpeciesTwoWeeks'] * 10 / df['duration']



    