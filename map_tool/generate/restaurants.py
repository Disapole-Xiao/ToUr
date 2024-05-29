import random
import json

def generate_restaurants(num_restaurants, min_lon, max_lon, min_lat, max_lat):
    """
    Generate a specified number of restaurants within a specified rectangular area.

    Args:
    - num_restaurants: Number of restaurants to generate.
    - min_lon, max_lon: Minimum and maximum longitude values for the rectangular area.
    - min_lat, max_lat: Minimum and maximum latitude values for the rectangular area.

    Returns:
    - restaurants: List of dictionaries representing generated restaurants.
    """
    restaurants = []
    for i in range(num_restaurants):
        lon = round(random.uniform(min_lon, max_lon), 6)
        lat = round(random.uniform(min_lat, max_lat), 6)
        rating = round(random.uniform(1, 5), 1)  # 随机生成1到5之间的一位小数
        popularity = random.randint(1, 999)  # 随机生成1到999之间的整数
        amenity = {
            "id": i,
            "name": "咖啡厅",
            "description": "",
            "type": "咖啡厅",
            "foods": [
                "蓝山咖啡",
                "卡布奇诺"
            ],
            "popularity": popularity,
            "rating": rating,
            "lon": lon,
            "lat": lat
        }
        restaurants.append(amenity)
    return restaurants

# Define the rectangular area boundaries
min_lon = 116.29946011424994
max_lon = 116.30894982236566
min_lat = 39.985182373909055
max_lat = 39.996297520391465

# Generate restaurants
num_restaurants = 30  # You can specify the number of restaurants you want to generate
restaurants = generate_restaurants(num_restaurants, min_lon, max_lon, min_lat, max_lat)

# Print generated restaurants
print("Generated Amenities:")
for amenity in restaurants:
    print(amenity)

# Save generated restaurants to a JSON file
with open("map_tool/json/restaurants.json", "w", encoding="utf-8") as f:
    json.dump({"restaurants": restaurants}, f, indent=4, ensure_ascii=False)

print("Generated restaurants saved to 'generated_restaurants.json' successfully!")
