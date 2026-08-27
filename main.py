import os, requests, subprocess
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

BASE_API_URL = os.getenv("BASE_API_URL")

import json

def get_data(api_url: str, path: str):
    headers = {
        "User-Agent": "Magic",
        "Accept": "application/json;q=0.9,*/*;q=0.8"
    }

    r = requests.get(api_url + path, headers=headers)
    r.status_code

    if r.status_code != 200:
        return None

    return r.json()

def transfer_to_csv(json_data: dict):
    try:
        df = pd.read_json("output/data.json")
        df.to_csv("/home/morris/Documents/Projects/Active/Magic/output/data.csv", encoding="utf-8", index=False)
    except Exception:
        return False
    return True

if __name__ == "__main__":  
    print("Requesting data")
    data = get_data(BASE_API_URL, "/sets")
    if (data == None):
        print("An error occured getting the data from the API...")
        exit(1)
    print("Succesfully requested data")
    print("Filtering Data")
    processed_data = []

    for set in data['data']:
        if set['set_type'] != "token" and set['set_type'] != "promo" and set['set_type'] != "funny" and set['set_type'] != "memorabilia":
            processed_data.append({
                "code": set['code'],
                "name": set['name'],
                "released": set['released_at'],
                "api_url": set['uri'],
                "icon_url": set['icon_svg_uri'],
            })
    print("Filtered data")
    print("Saving data to output/data.json")
    with open("output/data.json", mode="w") as file:
        file.write(json.dumps(processed_data))
    print("Saved data to output/data.json")
    print("Saving CSV data to output/data.csv")
    worked = transfer_to_csv(data)
    print(("Succesfully" if worked == True else "Incorrectly") + " saved CSV data to output/data.csv")

