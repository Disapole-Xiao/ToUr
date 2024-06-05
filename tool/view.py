import folium
import json

def connected_components(graph):
    def dfs(node, visited, component):
        visited.add(node['id'])
        component.append(node['id'])
        for neighbor in node['adj']:
            if neighbor['id'] not in visited:
                dfs(graph[neighbor['id']], visited, component)
    
    visited = set()
    components = []

    for node in graph:
        if node['id'] not in visited:
            component = []
            dfs(node, visited, component)
            components.append(component)
    
    return components

# 加载地图数据
map_id = 4
json_file_path = f'static/maps/{map_id}.json'  # 替换为你的JSON数据文件路径
with open(json_file_path, 'r', encoding="utf-8") as file:
    map_data = json.load(file)

# 创建Folium地图实例
m = folium.Map(location=[39.90, 116.39], zoom_start=15)

# 获取连通分量
components = connected_components(map_data["nodes"])

# 定义颜色列表
colors = ['red', 'green', 'blue', 'orange', 'purple', 'pink', 'gray', 'black']

# 为每个节点添加圆圈标记和Popup，并画出边
for i, component in enumerate(components):
    for node_id in component:
        node = map_data['nodes'][node_id]
        # 画出与当前节点相连的边
        for adj in node['adj']:
            try:
                adj_node = map_data['nodes'][adj['id']]
            except IndexError:
                print(f"Warning: Node {node['id']} has an invalid adjacent node ID {adj['id']}")
            if adj_node:
                folium.PolyLine(
                    locations=[[node['lat'], node['lon']], [adj_node['lat'], adj_node['lon']]],
                    color=colors[i % len(colors)],  # 使用循环来选择颜色
                    weight=5,
                    popup=folium.Popup(f"<div>congestion:{adj['congestion']}<br>distance:{adj['distance']}</div>", max_width=250),
                    opacity=adj['congestion']
                ).add_to(m)
    
    # 画出每个连通分量中的节点
    for node_id in component:
        node = map_data['nodes'][node_id]
        popup_html = f"""<div>Node ID: {node_id}<br>
        lat: {node['lat']}<br>
        lon: {node['lon']}<br>
        <button onclick="copyToClipboard('{node_id}')">Copy ID</button></div>"""
        popup = folium.Popup(popup_html, max_width=250)
        folium.Circle(
            location=[node['lat'], node['lon']],
            radius=2,
            weight=5,
            color=colors[i % len(colors)],  # 使用循环来选择颜色
            fill=True,
            popup=popup,
            ).add_to(m)

# 保存地图为HTML文件
map_html_path = f'tool/{map_id}.html'
m.save(map_html_path)

# 在保存的HTML文件末尾添加对外部JavaScript文件的引用
with open(map_html_path, 'a') as file:
    file.write('<script src="map_script.js"></script>\n')

print("json to html completed")
