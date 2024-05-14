import json

map_id = 2
json_file_path = f'static/maps/{map_id}.json' 

# 读取JSON文件
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 删除adj中id大于2000的点
for node in data['nodes']:
    node['adj'] = [adj for adj in node['adj'] if int(adj['id']) <= 2000]

# 删除adj为空的所有node
data['nodes'] = [node for node in data['nodes'] if node['adj']]

# 将更新后的数据写回JSON文件
with open(json_file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
