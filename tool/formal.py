import json
import random

map_id = 3
json_file_path = f"static/maps/{map_id}.json"

# 读取 JSON 文件
with open(json_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 遍历节点
for node in data["nodes"]:
    # 保留经纬度到小数点后六位
    node["lat"] = round(node["lat"], 6)
    node["lon"] = round(node["lon"], 6)

    # 遍历邻接节点
    for adj_node in node["adj"]:
        # 保留距离到小数点后一位
        adj_node["distance"] = round(adj_node["distance"], 1)
        # 随机生成拥堵程度（0-1之间的随机数）
        tem = round(random.random(), 1)
        while tem == 0.0:
            tem = round(random.random(), 1)
        adj_node["congestion"] = tem

# for attraction in data["attractions"]:
#     # 保留经纬度到小数点后六位
#     attraction["lat"] = round(attraction["lat"], 6)
#     attraction["lon"] = round(attraction["lon"], 6)

# for amenitie in data["amenities"]:
#     # 保留经纬度到小数点后六位
#     amenitie["lat"] = round(amenitie["lat"], 6)
#     amenitie["lon"] = round(amenitie["lon"], 6)

# for restaurant in data["restaurants"]:
#     # 保留经纬度到小数点后六位
#     restaurant["lat"] = round(restaurant["lat"], 6)
#     restaurant["lon"] = round(restaurant["lon"], 6)

# 写入新的 JSON 文件
with open(json_file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
