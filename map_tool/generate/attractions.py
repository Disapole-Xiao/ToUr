import json
import requests

def get_poi_data(keywords, city, bbox, output="json", key=None):
    """
    Function to fetch POI (Points of Interest) data from AMap API.

    Args:
    - keywords: Keywords for POI search (e.g., "景点").
    - city: City name for search.
    - bbox: Bounding box coordinates in the format of "min_longitude,min_latitude,max_longitude,max_latitude".
    - output: Desired output format ("json" or "xml").
    - key: AMap API key (optional).

    Returns:
    - poi_data: List of dictionaries containing POI data, each dictionary containing "name" and "location" keys.
    """

    # AMap API URL
    url = "https://restapi.amap.com/v3/place/polygon"

    # Parameters
    params = {
        "keywords": keywords,
        "city": city,
        "polygon": bbox,
        "output": output,
        "key": key
    }

    # Send GET request
    response = requests.get(url, params=params)
    i=0
    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        poi_data = []
        if data["status"] == "1":  # Status 1 indicates success
            pois = data["pois"]
            for poi in pois:
                poi_name = poi["name"]
                poi_location = poi["location"]
                poi_lon, poi_lat = map(float, poi_location.split(","))
                poi_data.append({
                    "id": i,  # You can set a unique ID for each attraction if needed
                    "name": poi_name,
                    "description": "",  # You can add description if available
                    "entr_point": [0],  # You can add entrance points if available
                    "lon": poi_lon,
                    "lat": poi_lat
                })
                i+=1
            return poi_data
        else:
            print("Error:", data["info"])
            return None
    else:
        print("Request failed:", response.status_code)
        return None

# Example usage
if __name__ == "__main__":
    # Set your AMap API key
    api_key = "62a046691a8d6f62978020dfee45fbf8"

    # Define search parameters
    keywords = "教学楼"
    city = "北京"
    bbox = "116.320957,39.994377,116.332892,39.999103"  # Bounding box for Peking University

    # Fetch POI data
    poi_data = get_poi_data(keywords, city, bbox, key=api_key)

    # Save POI data to a JSON file
    if poi_data:
        with open("map_tool/json/attractions.json", "w", encoding="utf-8") as f:
            json.dump({"attractions": poi_data}, f, indent=4, ensure_ascii=False)
