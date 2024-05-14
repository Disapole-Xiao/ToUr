import json
from map import Map
inf = float('inf')


def adjlist_distance(nodes):
    adj_list = [[] for _ in range(len(nodes))]

    for node in nodes:
        adjacencies = node["adj"]
        for adj in adjacencies:
            neighbor = adj["id"]
            weight = adj["distance"]
            adj_list[node["id"]].append((neighbor, weight))

    return adj_list

def adjlist_time(nodes):
    adj_list = [[] for _ in range(len(nodes))]

    for node in nodes:
        adjacencies = node["adj"]
        for adj in adjacencies:
            neighbor = adj["node"]
            distance=adj["distance"]
            congestion=adj["congestion"]
            weight = distance/congestion
            adj_list[node["id"]].append((neighbor, weight))

        del node["adj"]

    return adj_list

# 返回值是id序列
def route_sgl(cur_map: Map, start: int, end: int, mode: str) -> list:
    # 从 Map 中获取边存储到邻接表 adj_list 中
    if mode == 'distance':
        adj_list=adjlist_distance(cur_map.nodes)
    elif mode == 'time' :
        adj_list=adjlist_time(cur_map.nodes)
    
    # dijkstra
    M = len(adj_list)
    dist = [inf] * M
    visit = [1] * M
    path = [-1] * M
    dist[start] = 0
    temp = start
    while start != end:
        Min = inf
        Next = -1
        for neighbor, weight in adj_list[start]:
            if visit[start]  and dist[start] + weight < dist[neighbor]:
                dist[neighbor] = dist[start] + weight
                path[neighbor] = start
            if visit[start] and dist[neighbor] < Min:
                Min = dist[neighbor]
                Next = neighbor
        if Min == inf:
            break
        start = Next
        visit[start] = 0

    # 获取最短路径
    shortestPath = []
    print('visit:', [x[0] for x in enumerate(visit) if x[1] == 0])
    print('path:', {x[0]:x[1] for x in enumerate(path) if x[1] != -1})
    while end != temp:
        shortestPath.append(path[end])
        end = path[end]
    shortestPath.reverse()
    return shortestPath

if __name__ == "__main__":
    with open("static/maps/1.json", "r", encoding='utf-8') as f:
        jsonstr = f.read()
    map = Map(jsonstr)
    print(route_sgl(map, 0, 1, 'distance'))
