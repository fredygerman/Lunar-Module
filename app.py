from urllib.request import Request
from fastapi import FastAPI, HTTPException
import json
from typing import List
import os

ROOT_DIR = os.getcwd()

app = FastAPI()

# Load the game reserves data
with open(os.path.join(ROOT_DIR, "data/game_reserves.json"), "r") as f:
    game_reserves = json.load(f)

@app.get("/game-reserves/{region_name}", response_model=List[dict])
async def get_game_reserves_by_region(region_name: str):
    reserves = [reserve for reserve in game_reserves if reserve["region"].lower() == region_name.lower()]
    if not reserves:
        raise HTTPException(status_code=404, detail="No game reserves found for the given region")
    return reserves

@app.get("/region/{reserve_name}")
async def get_region_by_reserve(reserve_name: str):
    for reserve in game_reserves:
        _reserve_name = reserve_name.lower()
        if reserve["national_park"].lower() == _reserve_name or reserve['national_park'] in reserve_name.lower():
            return {"id": reserve["id"],"region": reserve["region"]}
    raise HTTPException(status_code=404, detail="Game reserve not found")

@app.post("/validate-destination")
async def validate_destination(request: Request):
    data = await request.json()
    destination_name = data.get("destination_name")
    if not destination_name:
        raise HTTPException(status_code=400, detail="destination_name is required")
    
    for reserve in game_reserves:
        if reserve["national_park"].lower() == destination_name.lower():
            return {"valid": True}
    return {"valid": False}