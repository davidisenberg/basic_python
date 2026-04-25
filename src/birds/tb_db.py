import duckdb
import pandas as pd
import datetime


con = duckdb.connect('top_birding.db')


def normalize_name(name: str) -> str:
    return name.lower().strip().replace(',', '').replace('  ', ' ')


def _today() -> str:
    return datetime.date.today().isoformat()


#------------
# Generic queries
#------------
def q(query: str):
    result = con.execute(query)
    df = result.fetchall()
    return pd.DataFrame(df, columns=[desc[0] for desc in result.description])


def does_exist(table: str):
    df = q("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = '" + table + "')")
    return df.iloc[0, 0]


def create_table(table: str, df):
    con.register(table, df)
    con.commit()


def append_table(table: str, df):
    con.register('_append_tmp', df)
    if not does_exist(table):
        con.execute(f"CREATE TABLE {table} AS SELECT * FROM _append_tmp")
    else:
        con.append(table, df)
    con.commit()


def _migrate():
    if not does_exist('locations'):
        con.execute("""
            CREATE TABLE locations (
                loc_name VARCHAR,
                lat DOUBLE,
                lng DOUBLE
            )
        """)
        con.commit()

    if not does_exist('drive_times'):
        con.execute("""
            CREATE TABLE drive_times (
                loc_name VARCHAR,
                hotspot_lat DOUBLE,
                hotspot_lng DOUBLE,
                duration DOUBLE
            )
        """)
        con.commit()
        # Migrate existing durations out of hotspots if present
        if does_exist('hotspots'):
            con.execute("""
                INSERT INTO drive_times (loc_name, hotspot_lat, hotspot_lng, duration)
                SELECT loc_name, lat, lng, duration FROM hotspots WHERE duration > 0
            """)
            con.commit()

    if does_exist('hotspots'):
        cols = q("SELECT column_name FROM information_schema.columns WHERE table_name = 'hotspots'")
        if 'fetched_date' not in cols['column_name'].values:
            con.execute("ALTER TABLE hotspots ADD COLUMN fetched_date VARCHAR DEFAULT NULL")
            con.commit()

    if does_exist('goldens'):
        cols = q("SELECT column_name FROM information_schema.columns WHERE table_name = 'goldens'")
        existing = cols['column_name'].values
        new_cols = {
            'numBirdsTwoWeeks': 'INT DEFAULT 0',
            'numHighValue':     'INT DEFAULT 0',
            'numRaptors':       'INT DEFAULT 0',
            'numWarblers':      'INT DEFAULT 0',
            'numShorebirds':    'INT DEFAULT 0',
            'numWaterfowl':     'INT DEFAULT 0',
            'weightedBirds':    'DOUBLE DEFAULT 0',
            'highValueNames':   "VARCHAR DEFAULT ''",
            'raptorNames':      "VARCHAR DEFAULT ''",
            'warblerNames':     "VARCHAR DEFAULT ''",
            'shorebirdNames':   "VARCHAR DEFAULT ''",
            'waterfowlNames':   "VARCHAR DEFAULT ''",
            'numChecklists':    'INT DEFAULT 0',
            'numContributors':  'INT DEFAULT 0',
        }
        for col, typedef in new_cols.items():
            if col not in existing:
                con.execute(f"ALTER TABLE goldens ADD COLUMN {col} {typedef}")
        con.commit()


_migrate()


#------------
# TAXONOMY
#------------
def get_local_taxonomy():
    return q("SELECT * FROM taxonomy")


#------------
# LOCATIONS
#------------
def get_location(name: str):
    norm = normalize_name(name)
    rows = con.execute("SELECT lat, lng FROM locations WHERE loc_name = ?", [norm]).fetchall()
    if not rows:
        return None
    return rows[0][0], rows[0][1]


def set_location(name: str, lat, lng):
    norm = normalize_name(name)
    con.execute("DELETE FROM locations WHERE loc_name = ?", [norm])
    con.execute("INSERT INTO locations VALUES (?, ?, ?)", [norm, lat, lng])
    con.commit()


#------------
# DRIVE TIMES
#------------
def get_duration(loc_name: str, lat, long):
    rows = con.execute(
        "SELECT duration FROM drive_times WHERE loc_name = ? AND hotspot_lat = ? AND hotspot_lng = ?",
        [loc_name, float(lat), float(long)]
    ).fetchone()
    return rows[0] if rows else 0


def set_duration(loc_name: str, lat, long, duration):
    con.execute("DELETE FROM drive_times WHERE loc_name = ? AND hotspot_lat = ? AND hotspot_lng = ?",
                [loc_name, float(lat), float(long)])
    con.execute("INSERT INTO drive_times VALUES (?, ?, ?, ?)",
                [loc_name, float(lat), float(long), float(duration)])
    con.commit()


#------------
# HOTSPOTS
#------------
def does_hotspot_exist(loc_name: str):
    rows = con.execute(
        "SELECT count(*) FROM hotspots WHERE loc_name = ? AND fetched_date = ?",
        [loc_name, _today()]
    ).fetchone()
    return rows[0] > 0


def invalidate_location(loc_name: str):
    con.execute("DELETE FROM hotspots WHERE loc_name = ?", [loc_name])
    con.execute("DELETE FROM goldens WHERE loc_name LIKE ?", [loc_name + '%'])
    con.commit()


def get_local_hotspots(loc_name: str):
    return q("SELECT * FROM hotspots WHERE loc_name = '" + loc_name + "'")


def get_optimized_hotspots(loc_name: str, max_num: int):
    return q(
        "SELECT * FROM hotspots WHERE loc_name = '" + loc_name + "' "
        "AND (numSpeciesAllTime > 150 OR distance_miles < 2) "
        "ORDER BY rank DESC LIMIT " + str(max_num)
    )


#------------
# GOLDENS
#------------
def does_golden_exist(loc_name: str):
    if not does_exist('goldens'):
        return False
    df = q("SELECT Count(*) FROM goldens WHERE loc_name = '" + loc_name + "'")
    return df.iloc[0, 0] > 0


def get_local_goldens(loc_name: str):
    return q("SELECT * FROM goldens WHERE loc_name = '" + loc_name + "'")


#------------
# CACHE RESETS
#------------
def reset_birds_cache():
    """Clear bird data (hotspots + goldens) but keep drive times and locations."""
    con.execute("DROP TABLE IF EXISTS hotspots")
    con.execute("DROP TABLE IF EXISTS goldens")
    con.commit()


def start_over_hotspots():
    """Clear everything including drive times and locations."""
    con.execute("DROP TABLE IF EXISTS hotspots")
    con.execute("DROP TABLE IF EXISTS goldens")
    con.execute("DELETE FROM drive_times")
    con.execute("DELETE FROM locations")
    con.commit()
