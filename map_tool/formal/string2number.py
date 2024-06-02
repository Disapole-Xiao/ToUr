import json

map_id = 4
json_file_path = f'static/maps/{map_id}.json'

# 读取JSON文件

with open(json_file_path, "r",encoding="utf-8") as file:
    data = json.load(file)

# 遍历attractions列表中的每一项
for attraction in data["attractions"]:
    # 将entr_point中的字符串转换为整数
    attraction["entr_point"][0] = int(attraction["entr_point"][0])
    # 将lon和lat中的字符串转换为浮点数
    attraction["lon"] = float(attraction["lon"])
    attraction["lat"] = float(attraction["lat"])

# 将修改后的数据写回到同一个JSON文件中
with open(json_file_path, "w",encoding="utf-8") as file:
    json.dump(data, file,ensure_ascii=False, indent=4)
