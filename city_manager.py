import geonamescache
from fuzzywuzzy import process

# Initialize geonamescache
gc = geonamescache.GeonamesCache()

def fetch_city_names():
    """Fetches a list of city names from geonamescache."""
    try:
        cities = gc.get_cities()
        return [city['name'] for city in cities.values()]
    except Exception as e:
        print(f"Error fetching city names: {e}")
        return []

def fuzzy_match_city(city_input, city_names):
    """Fuzzy match the input city name against known city names."""
    try:
        matched_city, score = process.extractOne(city_input, city_names)
        return matched_city if score >= 80 else None
    except Exception as e:
        print(f"Error matching city: {e}")
        return None
