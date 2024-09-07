from fastapi import FastAPI, HTTPException
import json
from typing import List

app = FastAPI()

# Load the game reserves data
with open("data/game_reserves.json", "r") as f:
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
        if reserve["name"].lower() == reserve_name.lower():
            return {"region": reserve["region"]}
    raise HTTPException(status_code=404, detail="Game reserve not found")

# ... existing code ...

