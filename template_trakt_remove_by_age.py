import requests
from datetime import datetime, timedelta

# Trakt API credentials
CLIENT_ID = "YOUR_TRAKT_CLIENT_ID"
CLIENT_SECRET = "YOUR_TRAKT_CLIENT_SECRET"
ACCESS_TOKEN = "YOUR_TRAKT_ACCESS_TOKEN"
USERNAME = "YOUR_TRAKT_USERNAME"
LIST_NAME = "YOUR_LIST_NAME"

# TMDb API Key (replace with your actual key)
TMDB_API_KEY = "YOUR_TMDB_API_KEY"

BASE_URL_TRAKT = "https://api.trakt.tv"
BASE_URL_TMDB = "https://api.themoviedb.org/3"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "trakt-api-version": "2",
    "trakt-api-key": CLIENT_ID,
}

def fetch_tmdb_first_aired(tmdb_id):
    """Fetch the first aired date from TMDb using the tmdb_id."""
    url = f"{BASE_URL_TMDB}/tv/{tmdb_id}?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        tmdb_data = response.json()
        return tmdb_data.get("first_air_date")  # Returns a string like '2023-05-05'
    print(f"Failed to fetch TMDb data for TMDb ID: {tmdb_id}")
    return None

def get_list_items():
    """Fetch items from the specified Trakt list."""
    url = f"{BASE_URL_TRAKT}/users/{USERNAME}/lists/{LIST_NAME}/items"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def remove_items_from_list(items_to_remove):
    """Remove specified items from the Trakt list."""
    url = f"{BASE_URL_TRAKT}/users/{USERNAME}/lists/{LIST_NAME}/items/remove"
    payload = {
        "shows": [{"ids": {"trakt": item["show"]["ids"]["trakt"]}} for item in items_to_remove]
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print("Items removed successfully.")
    else:
        print(f"Error removing items: {response.text}")

def filter_items_to_remove(items):
    """Filter items that aired more than 90 days ago using Trakt or TMDb data."""
    ninety_days_ago = datetime.now() - timedelta(days=90)
    items_to_remove = []

    for item in items:
        if "show" in item:
            show = item["show"]
            trakt_id = show["ids"]["trakt"]
            tmdb_id = show["ids"].get("tmdb")

            # Fetch detailed show data from Trakt
            url = f"{BASE_URL_TRAKT}/shows/{trakt_id}"
            response = requests.get(url, headers=HEADERS)
            if response.status_code == 200:
                detailed_show = response.json()
                first_aired = detailed_show.get("first_aired")

                # If Trakt doesn't provide first_aired, fetch from TMDb
                if not first_aired and tmdb_id:
                    first_aired = fetch_tmdb_first_aired(tmdb_id)

                if first_aired:
                    air_date = datetime.strptime(first_aired, "%Y-%m-%d")
                    print(f"Show: {show['title']}, First Aired: {air_date}, Meets Criteria: {air_date < ninety_days_ago}")
                    if air_date < ninety_days_ago:
                        items_to_remove.append(item)
                else:
                    print(f"Show: {show['title']} does not have a valid 'first_aired' date.")
            else:
                print(f"Failed to fetch detailed data for show: {show['title']}")
    return items_to_remove

def main():
    print("Fetching items from the list...")
    all_items = get_list_items()

    print("Filtering items to remove...")
    items_to_remove = filter_items_to_remove(all_items)

    if items_to_remove:
        print(f"Removing {len(items_to_remove)} items from the list...")
        remove_items_from_list(items_to_remove)
    else:
        print("No items to remove.")

if __name__ == "__main__":
    main()
