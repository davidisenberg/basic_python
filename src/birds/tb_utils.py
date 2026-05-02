import datetime
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from birds.ebird import get_ebird_taxonomy, get_ebird_hotspots, get_recent_obs, get_checklist_stats
from birds.tb_db import (
    create_table, does_exist, get_local_taxonomy, get_local_hotspots,
    does_hotspot_exist, append_table, get_optimized_hotspots,
    does_golden_exist, get_cached_golden_loc_ids, get_local_goldens,
    get_duration, set_duration, invalidate_location,
)
from geopy.distance import geodesic
from routing.routing import get_ride_time

RAPTOR_ORDERS    = {'Accipitriformes', 'Falconiformes', 'Strigiformes', 'Cathartiformes'}
SHOREBIRD_ORDER  = 'Charadriiformes'
WATERFOWL_ORDER  = 'Anseriformes'
WARBLER_FAMILY   = 'New World Warblers'
SPARROW_FAMILY   = 'New World Sparrows'
PIGEON_FAMILY    = 'Pigeons and Doves'

# eBird species codes — verify/extend at ebird.org/species/<code>
HIGH_VALUE_SPECIES = {
    'scatan',  # Scarlet Tanager
    'sumtan',  # Summer Tanager
    'indbun',  # Indigo Bunting
    'paibun',  # Painted Bunting
    'robgro',  # Rose-breasted Grosbeak
    'blugro',  # Blue Grosbeak
    'balori',  # Baltimore Oriole
    'orchor',  # Orchard Oriole
    'bobo',    # Bobolink
    'woothr',  # Wood Thrush
    'swathr',  # Swainson's Thrush
    'herthr',  # Hermit Thrush
    'veery',   # Veery
    'yebcuc',  # Yellow-billed Cuckoo
    'blbcuc',  # Black-billed Cuckoo
    'rthhum',  # Ruby-throated Hummingbird
}

WEIGHTS = {
    'high_value': 3.0,
    'raptor':     2.0,
    'warbler':    3.0,
    'shorebird':  1.5,
    'waterfowl':  0.7,
    'sparrow':    0.5,
    'pigeon':     0.5,
    'other':      1.0,
}


def get_tb_taxonomy():
    if does_exist("taxonomy"):
        return get_local_taxonomy()
    else:
        df = get_ebird_taxonomy()
        create_table("taxonomy", df)
        return df


def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).miles


def get_tb_hotspots(name: str, lat, long):
    if does_exist("hotspots"):
        if does_hotspot_exist(name):
            print("hotspot cache hit: " + name)
            return get_local_hotspots(name)
        else:
            print("hotspot cache stale, invalidating: " + name)
            invalidate_location(name)

    print("fetching ebird hotspots for: " + name)
    df = get_ebird_hotspots(lat, long)
    if 'subnational2Code' not in df.columns:
        df['subnational2Code'] = ''
    df['loc_name'] = name
    df['distance_miles'] = df.apply(lambda row: calculate_distance(row['lat'], row['lng'], lat, long), axis=1)
    df['rank'] = df['numSpeciesAllTime'] ** 3 / df['distance_miles']
    df['fetched_date'] = datetime.date.today().isoformat()

    df = df[['locId', 'locName', 'countryCode', 'subnational1Code', 'subnational2Code',
             'lat', 'lng', 'latestObsDt', 'numSpeciesAllTime', 'loc_name',
             'distance_miles', 'rank', 'fetched_date']]

    append_table("hotspots", df)
    return df


def get_ride_time_or_cached(name, lat1, long1, lat2, long2):
    duration = get_duration(name, lat1, long1)
    if duration == 0:
        duration = get_ride_time(lat1, long1, lat2, long2)
        if duration is not None:
            set_duration(name, lat1, long1, duration)
        else:
            duration = 5 * 60 * 60
            set_duration(name, lat1, long1, duration)
    return duration


def _names(obs, mask):
    if 'comName' not in obs.columns:
        return ''
    return ', '.join(obs[mask]['comName'].dropna().unique().tolist())


def compute_obs_stats(obs_df, taxonomy_df):
    empty = {'numSpeciesTwoWeeks': 0, 'numBirdsTwoWeeks': 0,
             'numHighValue': 0, 'numRaptors': 0, 'numWarblers': 0, 'numShorebirds': 0, 'numWaterfowl': 0,
             'weightedBirds': 0.0,
             'highValueNames': '', 'raptorNames': '', 'warblerNames': '', 'shorebirdNames': '', 'waterfowlNames': ''}

    if obs_df.empty or 'speciesCode' not in obs_df.columns:
        return empty

    obs = obs_df.copy()
    obs['howMany'] = obs['howMany'].fillna(1) if 'howMany' in obs.columns else 1

    if not taxonomy_df.empty and 'speciesCode' in taxonomy_df.columns:
        tax_cols = [c for c in ['speciesCode', 'order', 'familyComName'] if c in taxonomy_df.columns]
        obs = obs.merge(taxonomy_df[tax_cols], on='speciesCode', how='left')

    count  = obs['howMany']
    order  = obs.get('order', pd.Series('', index=obs.index)).fillna('')
    family = obs.get('familyComName', pd.Series('', index=obs.index)).fillna('')

    # High-value allowlist takes priority — these get 3× regardless of family
    is_high_value = obs['speciesCode'].isin(HIGH_VALUE_SPECIES)
    is_raptor     = order.isin(RAPTOR_ORDERS) & ~is_high_value
    is_warbler    = (family == WARBLER_FAMILY) & ~is_high_value
    is_shorebird  = (order == SHOREBIRD_ORDER) & ~is_high_value
    is_waterfowl  = (order == WATERFOWL_ORDER) & ~is_high_value
    is_sparrow    = (family == SPARROW_FAMILY) & ~is_high_value
    is_pigeon     = (family == PIGEON_FAMILY)  & ~is_high_value
    is_other      = ~(is_high_value | is_raptor | is_warbler | is_shorebird | is_waterfowl | is_sparrow | is_pigeon)

    weighted = (
        is_high_value.sum() * WEIGHTS['high_value'] +
        is_raptor.sum()     * WEIGHTS['raptor']     +
        is_warbler.sum()    * WEIGHTS['warbler']    +
        is_shorebird.sum()  * WEIGHTS['shorebird']  +
        is_waterfowl.sum()  * WEIGHTS['waterfowl']  +
        is_sparrow.sum()    * WEIGHTS['sparrow']    +
        is_pigeon.sum()     * WEIGHTS['pigeon']     +
        is_other.sum()      * WEIGHTS['other']
    )

    return {
        'numSpeciesTwoWeeks': len(obs),
        'numBirdsTwoWeeks':   int(count.sum()),
        'numHighValue':       int(is_high_value.sum()),
        'numRaptors':         int(is_raptor.sum()),
        'numWarblers':        int(is_warbler.sum()),
        'numShorebirds':      int(is_shorebird.sum()),
        'numWaterfowl':       int(is_waterfowl.sum()),
        'weightedBirds':      float(weighted),
        'highValueNames':     _names(obs, is_high_value),
        'raptorNames':        _names(obs, is_raptor),
        'warblerNames':       _names(obs, is_warbler),
        'shorebirdNames':     _names(obs, is_shorebird),
        'waterfowlNames':     _names(obs, is_waterfowl),
    }


def _format_goldens(df):
    df = df.copy()
    if 'golden_rank' not in df.columns:
        df['golden_rank'] = 0.0
    df['golden_rank'] = df['golden_rank'].replace([float('inf'), float('-inf')], 0.0).fillna(0.0)
    if 'duration' in df.columns:
        df['duration2'] = round(df['duration'] / 60 / 60, 1)
    else:
        df['duration2'] = None
    cols = ['locName', 'lat', 'lng', 'numSpeciesAllTime', 'distance_miles',
            'numSpeciesTwoWeeks', 'numBirdsTwoWeeks',
            'numHighValue', 'highValueNames',
            'numRaptors', 'raptorNames',
            'numWarblers', 'warblerNames',
            'numShorebirds', 'shorebirdNames',
            'numWaterfowl', 'waterfowlNames',
            'numChecklists', 'numContributors',
            'golden_rank', 'duration2']
    df = df[[c for c in cols if c in df.columns]]
    df = df.sort_values(by='golden_rank', ascending=False)
    lo, hi = df['golden_rank'].min(), df['golden_rank'].max()
    if hi > lo:
        df['score'] = (1 + 99 * (df['golden_rank'] - lo) / (hi - lo)).round().clip(1, 100).astype(int)
    else:
        df['score'] = 50
    return df


def _fetch_hotspot_data(row, taxonomy_df):
    obs = get_recent_obs(row['lat'], row['lng'])
    stats = compute_obs_stats(obs, taxonomy_df)
    num_cl, num_contrib = get_checklist_stats(row['locId'])
    return stats, num_cl, num_contrib


_STAT_KEYS = [
    'numSpeciesTwoWeeks', 'numBirdsTwoWeeks',
    'numHighValue', 'numRaptors', 'numWarblers', 'numShorebirds', 'numWaterfowl',
    'weightedBirds',
    'highValueNames', 'raptorNames', 'warblerNames', 'shorebirdNames', 'waterfowlNames',
]


def stream_tb_goldens(name: str, lat, long, max_num):
    """Generator yielding ('progress', dict) then ('done', DataFrame)."""
    get_tb_hotspots(name, lat, long)

    if does_golden_exist(name, max_num):
        print(f"golden cache hit: {name}")
        yield 'done', _format_goldens(get_local_goldens(name))
        return

    taxonomy_df = get_tb_taxonomy()
    df_candidates = get_optimized_hotspots(name, max_num)

    # Split into already-cached and new — avoids re-fetching eBird data we already have
    cached_ids = get_cached_golden_loc_ids(name)
    df_cached  = get_local_goldens(name) if cached_ids else pd.DataFrame()
    df_cached_in_set = (
        df_cached[df_cached['locId'].isin(df_candidates['locId'])]
        if not df_cached.empty else pd.DataFrame()
    )
    df_new = df_candidates[~df_candidates['locId'].isin(cached_ids)].copy()
    total_new = len(df_new)

    # All candidates already cached (fewer good spots than max_num)
    if total_new == 0:
        yield 'done', _format_goldens(df_cached_in_set)
        return

    results = [None] * total_new
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_idx = {
            executor.submit(_fetch_hotspot_data, row, taxonomy_df): i
            for i, (_, row) in enumerate(df_new.iterrows())
        }
        completed = 0
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            results[idx] = future.result()
            completed += 1
            yield 'progress', {'current': completed, 'total': total_new * 2, 'message': f'Bird data: {completed}/{total_new}'}

    for key in _STAT_KEYS:
        df_new[key] = [r[0][key] for r in results]
    df_new['numChecklists']   = [r[1] for r in results]
    df_new['numContributors'] = [r[2] for r in results]

    # Merge with any already-cached candidates for ranking + drive times
    frames = [f for f in [df_cached_in_set, df_new] if not f.empty]
    df_all = pd.concat(frames, ignore_index=True)
    n_cached_in_set = len(df_cached_in_set)

    checklist_factor = df_all['numChecklists'].clip(lower=1) ** 0.3

    # Preliminary ranking: distance proxy (~40 mph)
    duration_proxy = df_all['distance_miles'].clip(lower=0.1) * 90
    df_all['golden_rank'] = (
        df_all['numSpeciesTwoWeeks'] ** 2 * df_all['weightedBirds']
        * checklist_factor / (duration_proxy / 60 / 3)
    )
    yield 'preliminary', _format_goldens(df_all)

    # Drive times — cached rows are fast lookups; only truly new spots hit ORS
    total_all = len(df_all)
    durations = []
    for _, row in df_all.iterrows():
        duration = get_ride_time_or_cached(name, row['lat'], row['lng'], str(lat), str(long))
        durations.append(duration)
        n = len(durations)
        yield 'progress', {'current': total_new + n, 'total': total_new + total_all, 'message': f'Drive times: {n}/{total_all}'}

    df_all['duration'] = durations
    df_all['golden_rank'] = (
        df_all['numSpeciesTwoWeeks'] ** 2 * df_all['weightedBirds']
        * checklist_factor / (df_all['duration'] / 60 / 3)
    )

    # Persist only the newly fetched rows (include golden_rank so cache is complete)
    df_new['duration']    = durations[n_cached_in_set:]
    df_new['golden_rank'] = df_all['golden_rank'].iloc[n_cached_in_set:].values
    df_new['loc_name']    = name
    append_table("goldens", df_new.drop(columns=['fetched_date'], errors='ignore'))

    yield 'done', _format_goldens(df_all)


def get_tb_goldens(name: str, lat, long, max_num):
    for event_type, data in stream_tb_goldens(name, lat, long, max_num):
        if event_type == 'done':
            return data
