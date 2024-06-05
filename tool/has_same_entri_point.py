import json

# 加载JSON数据
with open('static/maps/4.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

attraction_entr_points = set()
duplicates = {}

# 遍历attractions
for attraction in data['attractions']:
    entr_point = attraction['entr_point'][0]
    if entr_point in attraction_entr_points:
        duplicates[entr_point] = duplicates.get(entr_point, []) + [attraction['name']]
    else:
        attraction_entr_points.add(entr_point)

# 输出重复的entr_point及其对应的attractions
for entr_point, attr_names in duplicates.items():
    print(f"Duplicate entr_point {entr_point} found in attractions: {', '.join(attr_names)}")

if not duplicates:
    print("No duplicate entr_point found.")