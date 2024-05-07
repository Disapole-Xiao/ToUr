import folium
import json

# 加载地图数据
map_id = 1
json_file_path = f'static/maps/{map_id}.json'  # 替换为你的JSON数据文件路径
with open(json_file_path, 'r',encoding="utf-8") as file:
    map_data = json.load(file)

# 检查地图数据中是否有节点，如果有，使用第一个节点的位置初始化地图
if map_data['nodes']:
    initial_location = [map_data['nodes'][0]['lat'], map_data['nodes'][0]['lon']]
else:
    initial_location = [39.90, 116.39]  # 如果没有节点，使用默认位置

# 创建Folium地图实例
m = folium.Map(location=initial_location, zoom_start=15)

# 为每个节点添加圆圈标记和Popup，并画出边
for node in map_data['nodes']:
    node_id = node['id']
    popup_html = f"""<div>Node ID: {node_id}<br>
    <button onclick="copyToClipboard('{node_id}')">Copy ID</button></div>"""
    popup = folium.Popup(popup_html, max_width=250)
    folium.Circle(
        location=[node['lat'], node['lon']],
        radius=1,
        color='blue',
        fill=True,
        popup=popup
    ).add_to(m)

    # 画出与当前节点相连的边
    for adj in node['adj']:
        adj_node = next((item for item in map_data['nodes'] if item['id'] == adj['id']), None)
        if adj_node:
            folium.PolyLine(
                locations=[[node['lat'], node['lon']], [adj_node['lat'], adj_node['lon']]],
                color='green',
                weight=1,
            ).add_to(m)

# 保存地图为HTML文件
map_html_path = f'tool/{map_id}.html'
m.save(map_html_path)

# 在保存的HTML文件末尾添加对外部JavaScript文件的引用
with open(map_html_path, 'a') as file:
    file.write('<script src="map_script.js"></script>\n')

print("json to html completed")