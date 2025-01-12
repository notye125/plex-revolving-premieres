import requests
from datetime import datetime, timedelta

# Trakt API credentials
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
ACCESS_TOKEN = "your_access_token"
USERNAME = "your_username"
LIST_NAME = "your_list_name"

BASE_URL_TRAKT = "https://api.trakt.tv"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "trakt-api-version": "2",
    "trakt-api-key": CLIENT_ID,
}

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

def test_trakt_connection():
    """Test connection to the Trakt API."""
    url = f"{BASE_URL_TRAKT}/users/me"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        print("Connection successful:", response.json())
    else:
        print("Connection failed:", response.status_code, response.text)

def filter_items_to_remove(items):
    """Filter items that aired more than 90 days ago using Trakt's first_aired data."""
    ninety_days_ago = datetime.now() - timedelta(days=90)
    items_to_remove = []

    for item in items:
        if "show" in item:
            show = item["show"]
            trakt_id = show["ids"]["trakt"]

            # Fetch detailed show data from Trakt
            url = f"{BASE_URL_TRAKT}/shows/{trakt_id}?extended=full"
            response = requests.get(url, headers=HEADERS)
            if response.status_code == 200:
                detailed_show = response.json()
                first_aired = detailed_show.get("first_aired")

                if first_aired:
                    air_date = datetime.strptime(first_aired.split("T")[0], "%Y-%m-%d")
                    print(f"Show: {show['title']}, First Aired: {air_date}, Meets Criteria: {air_date < ninety_days_ago}")
                    if air_date < ninety_days_ago:
                        items_to_remove.append(item)
                else:
                    print(f"Show: {show['title']} does not have a valid 'first_aired' date.")
            else:
             
