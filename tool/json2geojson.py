## 把json转换成geojson，便于在插件或者geojson.io查看

import json

def convert_json_to_geojson(input_path, output_path):
    # Load the JSON data from the file
    with open(input_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Function to switch latitude and longitude
    def switch_coordinates(lat, lon):
        return [lon, lat]

    # Prepare the GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # Process entrances
    entrance = data.get("extrance", {})
    geojson["features"].append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": switch_coordinates(entrance["lat"], entrance["lon"])
        },
        "properties": {
            "name": "Entrance",
            "description": "Main entrance of the zoo"
        }
    })

    # Process attractions, amenities, and restaurants
    def process_items(items, item_type):
        for item in items:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": switch_coordinates(item["coordinate"]["lat"], item["coordinate"]["lon"])
                },
                "properties": {
                    "name": item["name"],
                    "description": item.get("description", ""),
                    "type": item_type
                }
            }
            geojson["features"].append(feature)

    process_items(data.get("attractions", []), "Attraction")
    process_items(data.get("amenities", []), "Amenity")
    process_items(data.get("restaurant", []), "Restaurant")

    # Nodes to LineStrings
    nodes = data.get("nodes", [])
    node_dict = {node["id"]: node for node in nodes}

    for node in nodes:
        for adj in node.get("adj", []):
            if node_dict.get(adj["id"]):  # Ensure the destination node exists
                start = switch_coordinates(float(node["lat"]), float(node["lon"]))
                end = switch_coordinates(float(node_dict[adj["id"]]["lat"]), float(node_dict[adj["id"]]["lon"]))
                line_feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [start, end]
                    },
                    "properties": {
                        "description": f"Road from node {node['id']} to node {adj['id']}",
                        "distance": adj["distance"],
                        "congestion": adj["congestion"],
                        "bicycle": adj["bicycle"],
                        "motorbike": adj["motorbike"]
                    }
                }
                geojson["features"].append(line_feature)

    # Save the GeoJSON data to a file
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(geojson, file, ensure_ascii=False, indent=4)

# Example usage
convert_json_to_geojson("path_to_input_file.json", "path_to_output_file.geojson")
