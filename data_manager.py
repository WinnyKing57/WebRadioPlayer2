# data_manager.py
# This module will handle saving and loading application data,
# such as known stations and favorites.

import json
import os

DATA_DIR = "data"
KNOWN_STATIONS_FILE = os.path.join(DATA_DIR, "known_stations.json")
FAVORITES_FILE = os.path.join(DATA_DIR, "favorites.json")
CUSTOM_STATIONS_FILE = os.path.join(DATA_DIR, "custom_stations.json")

def ensure_data_dir_exists():
    """Ensures the data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created data directory: {DATA_DIR}")

def save_json_data(filepath, data):
    """Saves data to a JSON file."""
    ensure_data_dir_exists()
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filepath}")
        return True
    except IOError as e:
        print(f"Error saving data to {filepath}: {e}")
        return False

def load_json_data(filepath):
    """Loads data from a JSON file."""
    ensure_data_dir_exists()
    if not os.path.exists(filepath):
        return None # Or an empty list/dict, depending on expected data
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Data loaded from {filepath}")
        return data
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading data from {filepath}: {e}")
        return None # Or an empty list/dict

if __name__ == '__main__':
    # Example usage:
    ensure_data_dir_exists()

    # Test saving and loading known stations
    sample_stations = [{"name": "Test Radio", "url": "http://example.com/stream"}]
    save_json_data(KNOWN_STATIONS_FILE, sample_stations)
    loaded_stations = load_json_data(KNOWN_STATIONS_FILE)
    if loaded_stations:
        print(f"Loaded stations: {loaded_stations}")

    # Test saving and loading favorites
    sample_favorites = [{"name": "Favorite FM", "url": "http://fav.example.com/stream"}]
    save_json_data(FAVORITES_FILE, sample_favorites)
    loaded_favorites = load_json_data(FAVORITES_FILE)
    if loaded_favorites:
        print(f"Loaded favorites: {loaded_favorites}")
