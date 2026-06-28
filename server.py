from fastapi import FastAPI

app = FastAPI()

@app.get("/nearby")
def get_nearby(lat: float, lon: float):
    return {"ok": True}
