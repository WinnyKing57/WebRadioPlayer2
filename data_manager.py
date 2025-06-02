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

# --- Generic Settings Management ---
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

def load_settings():
    """Loads the entire settings dictionary."""
    # ensure_data_dir_exists() is called by load_json_data
    settings = load_json_data(SETTINGS_FILE)
    return settings if settings else {}

def save_settings(settings_dict):
    """Saves the entire settings dictionary."""
    # ensure_data_dir_exists() is called by save_json_data
    return save_json_data(SETTINGS_FILE, settings_dict)

def save_setting(key, value):
    """Saves a specific setting by key."""
    settings = load_settings()
    settings[key] = value
    return save_settings(settings)

def load_setting(key, default_value=None):
    """Loads a specific setting by key, returning default_value if not found."""
    settings = load_settings()
    return settings.get(key, default_value)

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

    # Test new settings functions
    print("\nTesting settings functions...")
    save_setting("test_setting1", "hello")
    save_setting("test_setting2", 123)
    loaded_setting1 = load_setting("test_setting1")
    loaded_setting2 = load_setting("test_setting2")
    loaded_setting3 = load_setting("non_existent_setting", "default")
    print(f"Loaded test_setting1: {loaded_setting1}") # Expected: hello
    print(f"Loaded test_setting2: {loaded_setting2}") # Expected: 123
    print(f"Loaded non_existent_setting: {loaded_setting3}") # Expected: default
    all_settings = load_settings()
    print(f"All settings: {all_settings}") # Expected: {'test_setting1': 'hello', 'test_setting2': 123}
