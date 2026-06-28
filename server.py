from fastapi import FastAPI
from geopy.distance import geodesic
import requests

app = FastAPI()

properties = []

# 1. Hämta data från riktig källa (ex Booli API)
def fetch_properties():
    global properties

    # OBS: här använder du riktig API-åtkomst (ingen scraping)
    url = "https://api.booli.se/listings"  # konceptuell endpoint

    response = requests.get(url)
    data = response.json()

    cleaned = []
    for item in data["listings"]:
        cleaned.append({
            "id": item["id"],
            "address": item["address"],
            "lat": item["lat"],
            "lon": item["lon"],
            "price": item["price"]
        })

    properties = cleaned


# 2. Kör enkel närhetslogik
def nearby(lat, lon, radius_km=3):
    user = (lat, lon)

    results = []

    for p in properties:
        dist = geodesic(user, (p["lat"], p["lon"])).km

        if dist <= radius_km:
            p_copy = p.copy()
            p_copy["distance"] = dist
            results.append(p_copy)

    return sorted(results, key=lambda x: x["distance"])


@app.get("/update")
def update():
    fetch_properties()
    return {"status": "updated", "count": len(properties)}


@app.get("/nearby")
def get_nearby(lat: float, lon: float):
    return nearby(lat, lon)
