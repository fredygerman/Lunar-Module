from fastapi import FastAPI, HTTPException, Request
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

@app.post("/validate-destination")
async def validate_destination(request: Request):
    data = await request.json()
    print(data)
    # destination_name = data.get("destination_name")
    # if not destination_name:
    #     raise HTTPException(status_code=400, detail="destination_name is required")
    
    # matching_reserves = []
    # for reserve in game_reserves:
    #     if destination_name.lower() in reserve["national_park"].lower():
    #         matching_reserves.append(reserve)
    
    # if not matching_reserves:
    #     return {"valid": False, "matches": []}
    
    # return {"valid": True, "matches": matching_reserves}
    return {"valid": True, "matches": []}
