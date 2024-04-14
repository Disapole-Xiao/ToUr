import json

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

# 读取JSON文件
with open('data/maps/1.json', 'r') as file:
    data = json.load(file)

# 从0开始编号并更新相关连接信息中的ID
for idx, node in enumerate(data['nodes']):
    old_id = node['id']
    new_id = str(idx)
    update_ids(data, old_id, new_id)

# 写回JSON文件
with open('data/maps/1.json', 'w') as file:
    json.dump(data, file, indent=4)
