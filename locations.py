# locations.py

# Dictionary of predefined locations (Name: (Latitude, Longitude))
LOCATIONS = {
    "Cumbria": (54.4609, -3.0886),
    "Corfe Castle": (50.6395, -2.0566),
    "The Cotswolds": (51.8330, -1.8433),
    "Cambridge": (52.2053, 0.1218),
    "Bristol": (51.4545, -2.5879),
    "Oxford": (51.7520, -1.2577),
    "Norwich": (52.6309, 1.2974),
    "Stonehenge": (51.1789, -1.8262),
    "Watergate Bay": (50.4429, -5.0553),
    "Birmingham": (52.4862, -1.8904)
}

# Function to retrieve coordinates
def get_coordinates(location_name):
    """
    Returns the latitude and longitude of a location if it exists.

    Args:
        location_name (str): Name of the location.

    Returns:
        tuple: (latitude, longitude) or None if not found.
    """
    return LOCATIONS.get(location_name, None)


# Function to return all available locations
def get_all_locations():
    """
    Returns all available locations.

    Returns:
        list: List of location names.
    """
    return list(LOCATIONS.keys())
