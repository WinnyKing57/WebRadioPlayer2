# radio_logic.py
import requests
import json # Added this as it was missing in previous full versions for JSONDecodeError
from data_manager import (
    load_json_data, save_json_data,
    KNOWN_STATIONS_FILE, FAVORITES_FILE, CUSTOM_STATIONS_FILE # Ensure CUSTOM_STATIONS_FILE is imported
)

RADIO_LIST_URL = "http://grutinny.ei.free.fr/audio/radio.json"

# --- Fetched Station Management ---
def fetch_radio_stations():
    """Fetches stations from URL."""
    try:
        print(f"Fetching radio stations from {RADIO_LIST_URL}...")
        response = requests.get(RADIO_LIST_URL, timeout=10)
        response.raise_for_status()
        stations = response.json()
        print(f"Successfully fetched {len(stations)} stations.")
        return stations
    except requests.exceptions.Timeout:
        print(f"Error fetching radio stations: Timeout for {RADIO_LIST_URL}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Error fetching radio stations: HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching radio stations: General Error: {e}")
        return None
    except json.JSONDecodeError as e: # Ensure json is imported
        print(f"Error fetching radio stations: Could not decode JSON: {e}")
        return None

def get_new_and_updated_stations(): # Renamed from original get_new_stations
    """
    Fetches stations, identifies new ones vs known, updates known stations list.
    Returns tuple: (all_fetched_stations, new_stations_list)
    """
    print("Checking for new/updated fetched stations...")
    fetched_stations = fetch_radio_stations()
    if fetched_stations is None:
        return None, []

    known_stations_list = load_json_data(KNOWN_STATIONS_FILE)
    if known_stations_list is None:
        known_stations_list = [] # Treat as empty if not found

    known_urls = {station['url'] for station in known_stations_list if 'url' in station}
    new_stations = []
    for station in fetched_stations:
        if station.get('url') not in known_urls:
            print(f"New fetched station: {station.get('name')}")
            new_stations.append(station)

    save_json_data(KNOWN_STATIONS_FILE, fetched_stations) # Always save the latest fetched list
    return fetched_stations, new_stations

# --- Favorites Management ---
def load_favorites():
    favorites = load_json_data(FAVORITES_FILE)
    return favorites if favorites else []

def save_favorites(favorites_list):
    return save_json_data(FAVORITES_FILE, favorites_list)

def is_favorite(station_url):
    return any(fav.get('url') == station_url for fav in load_favorites())

def add_to_favorites(station_data):
    if not isinstance(station_data, dict) or 'url' not in station_data or 'name' not in station_data:
        return False
    favorites = load_favorites()
    if not is_favorite(station_data['url']):
        favorites.append(station_data)
        save_favorites(favorites)
        print(f"Station '{station_data.get('name')}' added to favorites.")
        return True
    return False

def remove_from_favorites(station_url):
    favorites = load_favorites()
    original_count = len(favorites)
    favorites = [fav for fav in favorites if fav.get('url') != station_url]
    if len(favorites) < original_count:
        save_favorites(favorites)
        print(f"Station with URL '{station_url}' removed from favorites.")
        return True
    return False

# --- Custom Radio Station Management ---
def load_custom_stations():
    custom_stations = load_json_data(CUSTOM_STATIONS_FILE)
    return custom_stations if custom_stations else []

def save_custom_stations(custom_stations_list):
    return save_json_data(CUSTOM_STATIONS_FILE, custom_stations_list)

def add_custom_station(name, url):
    if not name or not url: return False
    custom_stations = load_custom_stations()
    if any(s.get('url') == url for s in custom_stations): return False

    new_station = {'name': name, 'url': url, 'custom': True}
    custom_stations.append(new_station)
    if save_custom_stations(custom_stations):
        print(f"Custom station '{name}' added.")
        return True
    return False

def get_all_display_stations():
    """Combines fetched and custom stations for UI display."""
    print("Getting all display stations (fetched + custom)...")
    fetched_stations, new_fetched_list = get_new_and_updated_stations()

    current_fetched_stations = fetched_stations if fetched_stations else []
    custom_stations_list = load_custom_stations()

    # Combine, prioritizing fetched if URL conflict (though custom shouldn't clash with live fetch often)
    # Marking custom stations is already done in add_custom_station.
    # Fetched stations don't have 'custom' key or it's False.

    combined_list = list(current_fetched_stations)
    fetched_urls = {s['url'] for s in current_fetched_stations if 'url' in s}

    for cs in custom_stations_list:
        if cs.get('url') not in fetched_urls:
            combined_list.append(cs)

    print(f"Combined list for display: {len(combined_list)} stations.")
    return combined_list, new_fetched_list


if __name__ == '__main__':
    import os
    import data_manager # For direct access to file paths if needed for cleanup

    print("--- Running radio_logic.py tests ---")
    data_manager.ensure_data_dir_exists() # Ensure data dir exists for all tests

    # --- Test Fetched Station Management ---
    print("\n--- Testing Fetched Station Management ---")
    # Clean known_stations.json for predictable "new" station count
    if os.path.exists(data_manager.KNOWN_STATIONS_FILE):
        os.remove(data_manager.KNOWN_STATIONS_FILE)
    fetched, new_f = get_new_and_updated_stations()
    if fetched: print(f"Fetched {len(fetched)} stations, {len(new_f)} new.")
    else: print("Failed to fetch stations for test.")
    # Run again to see if "new" count changes
    fetched_again, new_f_again = get_new_and_updated_stations()
    if fetched_again: print(f"Fetched {len(fetched_again)} stations again, {len(new_f_again)} new (expected 0).")


    # --- Test Favorites Management ---
    print("\n--- Testing Favorites Management ---")
    if os.path.exists(data_manager.FAVORITES_FILE): os.remove(data_manager.FAVORITES_FILE)
    s1 = {"name": "Fav Radio 1", "url": "http://fav1.com"}
    s2 = {"name": "Fav Radio 2", "url": "http://fav2.com"}
    add_to_favorites(s1); add_to_favorites(s2)
    print(f"Is fav1 favorite? {is_favorite(s1['url'])}") # True
    remove_from_favorites(s1['url'])
    print(f"Is fav1 favorite after remove? {is_favorite(s1['url'])}") # False
    print(f"Current favorites: {load_favorites()}")


    # --- Test Custom Station Management ---
    print("\n--- Testing Custom Station Management ---")
    if os.path.exists(data_manager.CUSTOM_STATIONS_FILE): os.remove(data_manager.CUSTOM_STATIONS_FILE)
    add_custom_station("Custom 1", "http://custom1.com")
    add_custom_station("Custom 2", "http://custom2.com")
    print(f"Custom stations: {load_custom_stations()}")

    # --- Test Combined Display ---
    print("\n--- Testing Combined Display (get_all_display_stations) ---")
    # Relies on previous KNOWN_STATIONS_FILE state from fetched test
    # For a clean test of 'new_fetched' part of get_all_display_stations:
    # if os.path.exists(data_manager.KNOWN_STATIONS_FILE): os.remove(data_manager.KNOWN_STATIONS_FILE)
    all_display_list, new_in_display = get_all_display_stations()
    if all_display_list:
        print(f"Total for display: {len(all_display_list)}, New fetched in this batch: {len(new_in_display)}")
        # for s_disp in all_display_list:
            # print(f"  - {s_disp.get('name')} (Custom: {s_disp.get('custom', False)})")
    else:
        print("get_all_display_stations returned no combined data.")

    print("\n--- All radio_logic.py tests complete ---")
