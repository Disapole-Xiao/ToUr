import json

map_id = 3

# 定义一个函数用于更新节点和连接信息的ID
def update_ids(data, old_id, new_id):
    # 更新节点ID
    for node in data['nodes']:
        if node['id'] == old_id:
            node['id'] = new_id

    # 更新连接信息中的ID
    for node in data['nodes']:
        for adj_node in node.get('adj', []):
            if adj_node['id'] == old_id:
                adj_node['id'] = new_id

def update_amenities_ids(data):
    new_id = 0
    for amenity in data['amenities']:
        amenity['id'] = new_id
        new_id += 1

def update_restaurants_ids(data):
    new_id = 0
    for restaurant in data['restaurants']:
        restaurant['id'] = new_id
        new_id += 1

def update_attractions_ids(data):
    new_id = 0
    for attraction in data['attractions']:
        attraction['id'] = new_id
        new_id += 1

# 读取JSON文件
with open('static/maps/{}.json'.format(map_id), 'r',encoding="utf-8") as file:
    data = json.load(file)

# 创建一个字典，用于存储旧ID和新ID之间的映射关系
id_mapping = {}

# 从0开始编号并更新相关连接信息中的ID
for idx, node in enumerate(data['nodes']):
    old_id = node['id']
    new_id = str(idx)
    id_mapping[old_id] = new_id
    update_ids(data, old_id, new_id)

# 更新attractions中的entr_point中的数字
for attraction in data['attractions']:
    old_point = attraction['entr_point'][0]
    new_point = id_mapping.get(str(old_point), None)
    if new_point is not None:
        attraction['entr_point'][0] = int(new_point)

update_amenities_ids(data)
update_restaurants_ids(data)
update_attractions_ids(data)

# 将更新后的数据写回JSON文件
with open('static/maps/{}.json'.format(map_id), 'w',encoding="utf-8") as file:
    json.dump(data, file,ensure_ascii=False, indent=4)
