import random
import json

def generate_amenities(min_lon, max_lon, min_lat, max_lat):
    """
    Generate a specified number of amenities within a specified rectangular area.

    Args:
    - num_amenities: Number of amenities to generate.
    - min_lon, max_lon: Minimum and maximum longitude values for the rectangular area.
    - min_lat, max_lat: Minimum and maximum latitude values for the rectangular area.

    Returns:
    - amenities: List of dictionaries representing generated amenities.
    """
    amenities = []
    name=["卫生间","喷泉","公共电话亭","外卖柜","商店","快递站","医务室","观景台","眼镜店","打印店"]
    num=[12,3,4,3,8,3,4,3,5,5]
    n=0
    for i in range(10):
        for j in range(num[i]):
            lon = round(random.uniform(min_lon, max_lon), 6)
            lat = round(random.uniform(min_lat, max_lat), 6)
            amenity = {
                "id": n,
                "name": f"{name[i]}{j}",
                "description": "",
                "type": f"{name[i]}",
                "lon": lon,
                "lat": lat
            }
            n+=1
            amenities.append(amenity)
    return amenities
    

# Define the rectangular area boundaries
min_lon = 116.32306830418179
max_lon = 116.33642270337396
min_lat = 39.937915601638736
max_lat = 39.94306012273515

# Generate amenities
# You can specify the number of amenities you want to generate
amenities = generate_amenities(min_lon, max_lon, min_lat, max_lat)

# Print generated amenities
print("Generated Amenities:")
for amenity in amenities:
    print(amenity)

# Save generated amenities to a JSON file
with open("map_tool/json/amenities.json", "w", encoding="utf-8") as f:
    json.dump({"amenities": amenities}, f, indent=4, ensure_ascii=False)

print("Generated amenities saved to 'generated_amenities.json' successfully!")
