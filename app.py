from fastapi import FastAPI, HTTPException
import json
from typing import List
import os

from utils.utilities import build_menu

ROOT_DIR = os.getcwd()

app = FastAPI()

# Load the game reserves data
with open(os.path.join(ROOT_DIR, "data/game_reserves.json"), "r") as f:
    game_reserves = json.load(f)

@app.post("/game-reserves/{region_name}", response_model=dict)
async def get_game_reserves_by_region(region_name: str):
    reserves = [reserve for reserve in game_reserves if reserve["region"].lower() == region_name.lower()]
    reserves = build_menu(
        body="Please select what game reserve that you are going to visit.",
        button="Game Reserve",
        title="Game reserves",
        rows=reserves
    )
    if not reserves:
        raise HTTPException(status_code=404, detail="No game reserves found for the given region")
    return reserves

@app.post("/region/{reserve_name}", response_model=dict)
async def get_region_by_reserve(reserve_name: str):
    for reserve in game_reserves:
        _reserve_name = reserve_name.lower()
        if reserve["national_park"].lower() == _reserve_name or reserve['national_park'] in reserve_name.lower():
            return {"id": reserve["id"],"region": reserve["region"]}
    raise HTTPException(status_code=404, detail="Game reserve not found")


