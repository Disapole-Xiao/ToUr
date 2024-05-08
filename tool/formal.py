import json
import random

# 读取 JSON 文件
with open('static/maps/1.json', 'r',encoding="utf-8") as f:
    data = json.load(f)

# 遍历节点
for node in data['nodes']:
    # 保留经纬度到小数点后六位
    node['lat'] = round(node['lat'], 6)
    node['lon'] = round(node['lon'], 6)
    
    # 遍历邻接节点
    for adj_node in node['adj']:
        # 保留距离到小数点后一位
        adj_node['distance'] = round(adj_node['distance'], 1)
        # 随机生成拥堵程度（0-1之间的随机数）
        adj_node['congestion'] = round(random.uniform(0, 1), 1)

for attraction in data['attractions']:
    # 保留经纬度到小数点后六位
    attraction['coordinate']['lat'] = round(attraction['coordinate']['lat'], 6)
    attraction['coordinate']['lon'] = round(attraction['coordinate']['lon'], 6)

for amenitie in data['amenities']:
    # 保留经纬度到小数点后六位
    amenitie['coordinate']['lat'] = round(amenitie['coordinate']['lat'], 6)
    amenitie['coordinate']['lon'] = round(amenitie['coordinate']['lon'], 6)

for restaurant in data['restaurants']:
    # 保留经纬度到小数点后六位
    restaurant['coordinate']['lat'] = round(restaurant['coordinate']['lat'], 6)
    restaurant['coordinate']['lon'] = round(restaurant['coordinate']['lon'], 6)

# 写入新的 JSON 文件
with open('static/maps/1.json', 'w',encoding="utf-8") as f:
    json.dump(data, f,ensure_ascii=False, indent=4)
