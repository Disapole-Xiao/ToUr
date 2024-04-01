'''
请你写一个py程序，将这个osm格式的地图转化为如下json格式规定的地图。
osm中删除地铁、高铁等属性的way，只保留只能步行、骑自行车或者电动车的道路。只能步行的道路"bicycle"、"motorbike"的属性都为false。能骑自行车或电动车的道路"bicycle"、"motorbike"的属性为true，false。 你需要自己判断哪种osm标签代表的道路能通行自行车或电动车或只能步行。
osm中的way拆成结点之间的两两关系，转化为node的邻接关系放在“adj”中。两点间的距离“distance”使用两点经纬度计算出来。“congestion”均设置为1.0
'''

from xml.etree import ElementTree as ET
import math
import json

# Load and parse the OSM file
map_id = 1
osm_file = f'tool/{map_id}.osm'
tree = ET.parse(osm_file)
root = tree.getroot()

# Function to calculate distance between two coordinates in meters
def calc_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = 6371000 * c  # Radius of Earth in meters
    return distance

# Process nodes
nodes = {}
for node in root.findall('node'):
    node_id = node.get('id')
    lat = float(node.get('lat'))
    lon = float(node.get('lon'))
    nodes[node_id] = {'id': node_id, 'lat': lat, 'lon': lon, 'adj': []}

# Placeholder to identify road types that are not allowed
excluded_highways = ['motorway', 'trunk', 'railway','secondary']

# Process ways
for way in root.findall('way'):
    highway = None
    bicycle, motorbike = None, None  # Default to None before checking
    for tag in way.findall('tag'):
        k = tag.get('k')
        v = tag.get('v')
        if k == 'highway':
            highway = v
        elif k == 'bicycle':
            bicycle = (v == 'yes')
        elif k == 'motorbike':
            motorbike = (v == 'yes')
    
    # If this is an excluded highway type or not a highway at all, skip it
    if highway in excluded_highways or not highway:
        continue
    
    # Determine if the way is accessible by bicycle or motorbike
    if bicycle is None:  # If not explicitly mentioned, determine by highway type
        bicycle = highway not in ['footway', 'steps', 'path']
    if motorbike is None:
        motorbike = bicycle  # Assuming motorbike access matches bicycle if unspecified

    # Convert way to node adjacencies
    way_nodes = way.findall('nd')
    for i in range(len(way_nodes)-1):
        node_id_1 = way_nodes[i].get('ref')
        node_id_2 = way_nodes[i+1].get('ref')
        if node_id_1 in nodes and node_id_2 in nodes:
            lat1, lon1 = nodes[node_id_1]['lat'], nodes[node_id_1]['lon']
            lat2, lon2 = nodes[node_id_2]['lat'], nodes[node_id_2]['lon']
            distance = calc_distance(lat1, lon1, lat2, lon2)
            # Append adjacency info
            nodes[node_id_1]['adj'].append({
                'id': node_id_2,
                'distance': distance,
                'congestion': 1.0,
                'bicycle': bicycle,
                'motorbike': motorbike
            })

# 删除孤立点
delete_id = [] 
for node_id in nodes:
    if not nodes[node_id]['adj']:
        delete_id.append(node_id)
for id in delete_id: del nodes[id]

# Prepare the list of nodes for JSON output (remove node IDs as they are redundant in this structure)
nodes_list = list(nodes.values())
print("node num:", len(nodes_list))

# Since the nodes_list is potentially large, we will not print it directly to avoid overwhelming the output
# Instead, we'll convert it to JSON and save it to a file
json_output_path = f'data/maps/{map_id}.json'
with open(json_output_path, 'w') as json_file:
    json.dump({'nodes': nodes_list}, json_file, ensure_ascii=False, indent=4)

