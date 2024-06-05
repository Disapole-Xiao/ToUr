import json

def connected_components(graph):
    def dfs(node, visited, component):
        visited.add(node['id'])
        component.append(node['id'])
        for neighbor in node['adj']:
            if neighbor['id'] not in visited:
                dfs(graph[neighbor['id']], visited, component)
    
    # 初始化一个空集合来跟踪已访问的节点
    visited = set()
    components = []

    for node in graph:
        if node['id'] not in visited:
            component = []
            dfs(node, visited, component)
            components.append(component)
    
    return components

with open("static/maps/4.json", "r", encoding="utf-8") as f:
    jsonstr = f.read()
map = json.loads(jsonstr)

# 获取连通分量
components = connected_components(map["nodes"])

# 打印每个连通分量的id
for i, component in enumerate(components):
    print("连通分量 {}: {}".format(i+1, component))
