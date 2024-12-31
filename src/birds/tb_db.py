import duckdb
import pandas as pd


con = duckdb.connect('top_birding.db')

#------------
# Generic queries
#------------
def q( query: str):
    
    result = con.execute(query)
    df = result.fetchall()
    df = pd.DataFrame(df, columns=[desc[0] for desc in result.description])

    return df


def does_exist( table: str ):
    df = q("select exists (SELECT 1 FROM information_schema.tables WHERE table_name = '" + table + "')")
    return df.iloc[0, 0]
    
def create_table(table: str, df):
    con.register(table, df)
    con.commit()


def append_table(table: str, df):
    con.append(table, df)
    con.commit()


def start_over_hotspots():
    con.execute("DROP TABLE hotspots")
    con.execute("DROP TABLE goldens")
    con.commit()

#------------
# TAXONOMY
#------------
def get_local_taxonomy():
    df = q("SELECT * FROM taxonomy")
    return df

#------------
# HOTSPOTS
#------------
def does_hotspot_exist(loc_name: str):
    df = q("SELECT count(*) FROM hotspots where loc_name = '" + loc_name + "'")
    return df.iloc[0, 0] > 0

def get_local_hotspots(loc_name: str):
    df = q("SELECT * FROM hotspots where loc_name = '" + loc_name + "'")
    return df

def get_optimized_hotspots(loc_name: str, max_num: int):
    df = q("select * from hotspots where (loc_name = '" + loc_name + "') and ((numSpeciesAllTime > 150) or (distance_miles < 2)) order by rank desc limit " + str(max_num))
    return df

def get_duration(loc_name: str, lat, long ):
    df = q("SELECT duration FROM hotspots where loc_name = '" + loc_name + "' and lat = '" + str(lat) + "' and lng = '" + str(long) + "'")
    return df.iloc[0, 0]

def set_duration(loc_name: str, lat, long, duration ):
    con.execute("UPDATE hotspots SET duration = '" + str(duration) + "' where loc_name = '" + loc_name + "' and lat = '" + str(lat) + "' and lng = '" + str(long) + "'")
    con.commit()



#------------
# GOLDENS
#------------
def does_golden_exist(loc_name: str):
    df = q("SELECT Count(*) FROM goldens where loc_name = '" + loc_name + "'")
    return df.iloc[0, 0] > 0

def get_local_goldens(loc_name: str):
    df = q("SELECT * FROM goldens where loc_name = '" + loc_name + "'")
    return df


def create_hotspot_tables():

    # Connect to a DuckDB database file
    con = duckdb.connect(database='top_birding.db')

    #start_over_hotspots()

    # Create a table
    con.execute("""
    CREATE TABLE hotspots (
    locId VARCHAR,	
    locName	VARCHAR,
    countryCode	VARCHAR,
    subnational1Code VARCHAR,	
    subnational2Code VARCHAR,	
    lat	DOUBLE,
    lng	DOUBLE,
    latestObsDt	VARCHAR,
    numSpeciesAllTime INT,	
    loc_name VARCHAR,
    distance_miles DOUBLE,
    duration DOUBLE,	
    rank DOUBLE,

    )
    """)

    # Commit the changes
    con.commit()

    con.execute("""
    CREATE TABLE goldens (
    locId VARCHAR,	
    locName	VARCHAR,
    countryCode	VARCHAR,
    subnational1Code VARCHAR,	
    subnational2Code VARCHAR,	
    lat	DOUBLE,
    lng	DOUBLE,
    latestObsDt	VARCHAR,
    numSpeciesAllTime INT,	
    loc_name VARCHAR,
    distance_miles DOUBLE,
    duration DOUBLE,	
    rank DOUBLE,
    numSpeciesTwoWeeks INT,
    golden_rank DOUBLE

    )
    """)


    # Close the connection
    con.close()