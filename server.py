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


from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
return """ <!DOCTYPE html> <html> <head> <title>Housing Radar</title> </head> <body> <h1>Housing Radar</h1>

```
    <button onclick="findNearby()">
        Hitta objekt nära mig
    </button>

    <pre id="result"></pre>

    <script>
    async function findNearby() {

        navigator.geolocation.getCurrentPosition(
            async function(position) {

                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                const response =
                    await fetch(
                        `/nearby?lat=${lat}&lon=${lon}`
                    );

                const data = await response.json();

                document.getElementById("result")
                    .textContent =
                    JSON.stringify(data, null, 2);
            },
            function(error) {
                alert("GPS nekades eller misslyckades");
            }
        );
    }
    </script>

</body>
</html>
"""
```

app.get("/update")
def update():
    fetch_properties()
    return {"status": "updated", "count": len(properties)}


# @app.get("/nearby")
# def get_nearby(lat: float, lon: float):
#   return nearby(lat, lon)

@app.get("/nearby")
def get_nearby(lat: float, lon: float):
return {
"latitude": lat,
"longitude": lon,
"properties_loaded": len(properties)
}

