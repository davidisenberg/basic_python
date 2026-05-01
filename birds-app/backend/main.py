import sys
import os
import re
import json
import secrets
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))
os.chdir(os.path.join(os.path.dirname(__file__), "../../src/birds"))

import airportsdata
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from geopy.geocoders import Nominatim
from birds.tb_utils import get_tb_goldens, stream_tb_goldens
from birds.tb_db import get_location, set_location, normalize_name, log_search, get_searches, get_search_stats

_airports = airportsdata.load('IATA')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "null"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

_ADMIN_KEY = os.environ.get('ADMIN_KEY', '')


def _require_admin(key: str):
    if not _ADMIN_KEY or not key or not secrets.compare_digest(key, _ADMIN_KEY):
        raise HTTPException(status_code=401, detail="Unauthorized")

geocoder = Nominatim(user_agent="top-birding-app")

if __name__ == "__main__":
    import argparse
    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument('--reset-cache', action='store_true', help='Clear all cached data including drive times')
    parser.add_argument('--reset-birds', action='store_true', help='Clear bird data only, keep drive times and locations')
    args = parser.parse_args()

    if args.reset_cache:
        from birds.tb_db import start_over_hotspots
        start_over_hotspots()
        print("Full cache cleared.")
    elif args.reset_birds:
        from birds.tb_db import reset_birds_cache
        reset_birds_cache()
        print("Bird cache cleared (drive times preserved).")

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)


def _location_type(location: str) -> str:
    if re.match(r'^\d{5}$', location.strip()):
        return 'zip'
    if re.match(r'^[A-Za-z]{3}$', location.strip()):
        return 'airport'
    return 'freeform'


def _resolve_location(location: str):
    norm = normalize_name(location)
    cached = get_location(norm)
    if cached:
        print(f"location cache hit: {norm}")
        return norm, cached[0], cached[1]

    # Airport code: exactly 3 letters
    code = location.strip().upper()
    if re.match(r'^[A-Z]{3}$', code) and code in _airports:
        ap = _airports[code]
        lat, lon = float(ap['lat']), float(ap['lon'])
        set_location(norm, lat, lon)
        print(f"airport lookup: {code} -> {lat}, {lon}")
        return norm, lat, lon

    # Zip code or freeform address: use Nominatim
    # Restrict 5-digit codes to the US — bare zip codes are ambiguous internationally
    is_zip = bool(re.match(r'^\d{5}$', location.strip()))
    geo = geocoder.geocode(location, country_codes='us' if is_zip else None)
    if geo is None:
        return None, None, None
    lat, lon = geo.latitude, geo.longitude
    set_location(norm, lat, lon)
    print(f"geocoded and cached: {norm} -> {lat}, {lon}")
    return norm, lat, lon


@app.get("/api/goldens/stream")
def stream_goldens(
    location: str = Query(..., description="Location name, e.g. 'Hoboken NJ'"),
    max_num: int = Query(20, ge=1, le=200),
):
    norm, lat, lon = _resolve_location(location)
    if norm is None:
        raise HTTPException(status_code=404, detail=f"Could not geocode '{location}'")

    log_search(location, _location_type(location), lat, lon, max_num)

    def generate():
        try:
            for event_type, data in stream_tb_goldens(norm, lat, lon, max_num):
                if event_type == 'progress':
                    yield f"data: {json.dumps(data)}\n\n"
                elif event_type == 'preliminary':
                    records = data.to_dict(orient='records')
                    payload = {'preliminary': True, 'location': location, 'lat': lat, 'lon': lon, 'results': records}
                    yield f"data: {json.dumps(payload)}\n\n"
                else:
                    records = data.to_dict(orient='records')
                    payload = {'done': True, 'location': location, 'lat': lat, 'lon': lon, 'results': records}
                    yield f"data: {json.dumps(payload)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/goldens")
def get_goldens(
    location: str = Query(..., description="Location name, e.g. 'Hoboken NJ'"),
    max_num: int = Query(20, ge=1, le=200),
):
    norm, lat, lon = _resolve_location(location)
    if norm is None:
        raise HTTPException(status_code=404, detail=f"Could not geocode '{location}'")

    df = get_tb_goldens(norm, lat, lon, max_num)
    return {"location": location, "lat": lat, "lon": lon, "results": df.to_dict(orient="records")}


@app.get("/api/admin/stats")
def admin_stats(key: str = Query(...)):
    _require_admin(key)
    return get_search_stats()


@app.get("/api/admin/searches")
def admin_searches(
    key: str = Query(...),
    limit: int = Query(1000, ge=1, le=5000),
    location_type: Optional[str] = Query(None),
):
    _require_admin(key)
    df = get_searches(limit, location_type)
    df['searched_at'] = df['searched_at'].astype(str)
    return df.to_dict(orient='records')


# Serve the built React frontend — must be mounted last so API routes take priority
_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
_frontend_dist = os.path.join(_BACKEND_DIR, "../frontend/dist")
if os.path.isdir(_frontend_dist):
    app.mount("/", StaticFiles(directory=_frontend_dist, html=True), name="static")
