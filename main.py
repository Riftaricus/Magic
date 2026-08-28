import pandas as pd
import json
import requests
import datetime
import colorama
from pathlib import Path

EXCLUDED_SET_TYPES = {"token", "promo", "funny", "memorabilia"}

BASE_API_URL = "https://api.scryfall.com"

HEADERS = {
    "User-Agent": "Magic/SkillHeroes/Morris",
    "Accept": "application/json;q=0.9,*/*;q=0.8",
}

OUTPUT_DIR = Path("output")
JSON_FILE = OUTPUT_DIR / "data.json"
CSV_FILE = OUTPUT_DIR / "data.csv"

def log(message: str, color: str = colorama.Fore.WHITE) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{color}[{timestamp}] {message}{colorama.Style.RESET_ALL}")

def fetch_sets() -> list[dict]:
    log("Requesting data from Scryfall API", colorama.Fore.GREEN)

    try:
        response = requests.get(
            f"{BASE_API_URL}/sets",
            headers=HEADERS,
            timeout=10,
        )
        response.raise_for_status()

    except requests.RequestException as error:
        log(f"Failed to request Scryfall API: {error}", colorama.Fore.RED)
        raise

    log(
        f"Successfully requested data with status code "
        f"{response.status_code}",
        colorama.Fore.GREEN,
    )

    return response.json()["data"]

def process_sets(sets: list[dict]) -> list[dict]:
    log("Filtering data on set_type", colorama.Fore.GREEN)

    processed_sets = []

    for index, set_data in enumerate(sets, start=1):
        if set_data["set_type"] in EXCLUDED_SET_TYPES:
            continue

        processed_sets.append(
            {
                "code": set_data["code"],
                "name": set_data["name"],
                "released": set_data["released_at"],
                "api_url": set_data["uri"],
                "icon_url": set_data["icon_svg_uri"],
            }
        )

        if index % 100 == 0:
            log(
                f"Processed {index}/{len(sets)} sets",
                colorama.Fore.GREEN,
            )

    log(
        f"Successfully processed {len(sets)} sets",
        colorama.Fore.GREEN,
    )

    log(
        f"There are now {len(processed_sets)} official sets left",
        colorama.Fore.GREEN,
    )

    return processed_sets

def save_json(data: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    log(f"Dumped data into '{path}'", colorama.Fore.GREEN)


def save_csv(data: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(data)
    df.to_csv(path, encoding="utf-8", index=False)

    log(f"Dumped data into '{path}'", colorama.Fore.GREEN)

def main() -> None:
    colorama.just_fix_windows_console()

    log("Running program", colorama.Fore.GREEN)

    sets = fetch_sets()
    processed_sets = process_sets(sets)

    log("Saving JSON data", colorama.Fore.GREEN)
    save_json(processed_sets, JSON_FILE)

    log("Saving CSV data", colorama.Fore.GREEN)
    save_csv(processed_sets, CSV_FILE)

    log("Successfully finished creating the CSV and JSON files", colorama.Fore.GREEN)

if __name__ == "__main__":
    main()