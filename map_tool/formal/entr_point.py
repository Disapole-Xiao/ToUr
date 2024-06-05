import json
from math import radians, sin, cos, sqrt, atan2

map_id = 4
json_file_path = f'static/maps/{map_id}.json' 

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Function to calculate the distance (in meters) between two points given their latitude and longitude.
    This function uses the Haversine formula.

    Args:
    - lat1, lon1: Latitude and longitude of point 1 (in degrees).
    - lat2, lon2: Latitude and longitude of point 2 (in degrees).

    Returns:
    - distance: Distance between the two points in meters.
    """
    # Radius of the Earth in meters
    R = 6371000.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Calculate the differences between latitudes and longitudes
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Calculate the Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Load JSON data
with open(json_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract attractions and nodes data
attractions = data["attractions"]
nodes = data["nodes"]

# Iterate over attractions
for attraction in attractions:
    min_distance = float('inf')
    nearest_node_id = None
    for node in nodes:
        distance = calculate_distance(attraction["lat"], attraction["lon"], node["lat"], node["lon"])
        if distance < min_distance:
            min_distance = distance
            nearest_node_id = node["id"]
    attraction["entr_point"] = [nearest_node_id]

# Save updated data to JSON file
with open(json_file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Updated JSON file saved successfully!")
