import json

def ensure_edge(map_id):
    # Load the JSON data from the file
    file_path = f'static/maps/{map_id}.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extract the nodes part
    nodes = data['nodes']

    # Checking for bidirectionality and removing duplicates
    for node in nodes:
        seen = set()
        new_adj = []
        for adj in node['adj']:
            if adj['id'] not in seen:
                seen.add(adj['id'])
                # Check for reverse path
                target_node = nodes[adj['id']]
                reverse_path = any(adjacency['id'] == node['id'] for adjacency in target_node['adj'])
                if not reverse_path:
                    # If reverse path doesn't exist, add it
                    target_node['adj'].append({
                        'id': node['id'],
                        'distance': adj['distance'],
                        'congestion': adj['congestion'],
                        'bicycle': adj['bicycle'],
                        'motorbike': adj['motorbike']
                    })
                new_adj.append(adj)
        node['adj'] = new_adj

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f'map {map_id} checked')

if __name__ == '__main__':
    ensure_edge(1)
    ensure_edge(2)
    ensure_edge(3)
    ensure_edge(4)