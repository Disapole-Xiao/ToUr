import json
inf = float('inf')

class Map:
    def __init__(self, mapid) -> None:
        with open(f"data/maps/{mapid}.json", 'r',encoding="utf-8") as fp:
            dic = json.load(fp)
        self.attractions = dic["attractions"]
        self.amenities = dic["amenities"]
        self.restaurants = dic["restaurants"]
        self.nodes = dic["nodes"]
        self.adjlist = []
        for node in self.nodes:
            self.adjlist.append(node["adj"])
            del node["adj"]

def adjlist_distance(nodes):
    adj_list = [[] for _ in range(len(nodes))]

    for node in nodes:
        adjacencies = node["adj"]
        for adj in adjacencies:
            neighbor = adj["node"]
            weight = adj["distance"]
            adj_list[node["id"]].append((neighbor, weight))

        del node["adj"]

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

def route_sgl(cur_map: Map, start: int, end: int, mode=0|1) -> list:
    # 从 Map 中获取边存储到邻接表 adj_list 中
    if mode==0:
        adj_list=adjlist_distance(cur_map.adjlist)
    else :
        adj_list=adjlist_time(cur_map.adjlist)
    
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
    while end != temp:
        shortestPath.append(path[end])
        end = path[end]
    shortestPath.reverse()
    return shortestPath
