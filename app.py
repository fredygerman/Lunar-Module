from fastapi import FastAPI, HTTPException, Request
import json
from typing import List
import aiohttp
import asyncio
import os

from utils.utilities import build_menu

ROOT_DIR = os.getcwd()

app = FastAPI()

# Load the game reserves data
with open(os.path.join(ROOT_DIR, "data/game_reserves.json"), "r") as f:
    game_reserves = json.load(f)

@app.post("/game-reserves", response_model=dict)
async def get_game_reserves_by_region(data: dict):
    region_name = data.get('region_name')
    reserves = [reserve for reserve in game_reserves if reserve["region"].lower() == region_name.lower()][:5]
    reserves = build_menu(
        body="Please select what game reserve that you are going to visit.",
        button="Game Reserve",
        title="Game reserves",
        rows=reserves
    )
    if not reserves:
        return {"text": "Sorry, your option is not available at the moment please write region name like Arusha, Dodoma etc"}

@app.post("/validate-destination")
async def validate_destination(data: dict):
    print("Data received: ", data)
    destination_name = data.get("destination_name")
    if not destination_name:
        raise HTTPException(status_code=400, detail="destination_name is required")
    
    matching_reserves = []
    for reserve in game_reserves:
        if destination_name.lower() in reserve["national_park"].lower():
            matching_reserves.append(reserve)
    
    if not matching_reserves:
        return {"valid": False, "matches": []}
    
    return {"valid": True, "matches": matching_reserves}


# Identify webhook, takes in phone number and calls user profile API to get user with that phone.
# If there is no user, call register user.
# Example:
# GET USER: https://7d66-197-250-226-171.ngrok-free.app/user/0745676696
# If null, create user:
# POST: https://7d66-197-250-226-171.ngrok-free.app/user
# BODY: {"phone": "0745676696"}
@app.post("/identify")
async def identify_user(data: dict):
    phone_number = data.get("phone")
    if not phone_number:
        return {"error": "Phone number is required"}

    user_url = f"https://7d66-197-250-226-171.ngrok-free.app/user/{phone_number}"
    async with aiohttp.ClientSession() as session:
        async with session.get(user_url) as response:
            if response.status == 200:
                user = await response.json()
                if user:
                    return user
            elif response.status != 404:
                return {"error": "Failed to fetch user"}

        # If user not found, create a new user
        create_user_url = "https://7d66-197-250-226-171.ngrok-free.app/user"
        async with session.post(create_user_url, json={"phone": phone_number}) as response:
            if response.status == 201:
                new_user = await response.json()
                return new_user
            else:
                return {"error": "Failed to create user"}


@app.post("/region", response_model=dict)
async def get_region_by_reserve(data: dict):
    reserve_name = data.get('reserve_name')
    for reserve in game_reserves:
        _reserve_name = reserve_name.lower()
        if reserve["national_park"].lower() == _reserve_name or reserve['national_park'] in reserve_name.lower():
            return {"id": reserve["id"],"region": reserve["region"]}
    raise {"text":"Game reserve not found, you can try "}



