from itertools import permutations
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
    
def getpath(a, b, path, anspath, idx):
    if path[a][b] == -1:
        return
    else:
        k = path[a][b]
        getpath(a, k, path, anspath, idx)
        anspath[idx[0]] = k
        idx[0] += 1
        getpath(k, b, path, anspath, idx)

def route_mul(cur_map: Map, nodes: list, start: int, mode=0 | 1) -> list:
    # 获取所需数据：dist矩阵，存储任意两点间的距离
    n = len(cur_map.nodes)
    dist = [[inf for _ in range(n)] for _ in range(n)]
    path = [[inf for _ in range(n)] for _ in range(n)]
    for node in nodes :
        adjacencies = node["adj"]
        now = nodes["id"]
        for adj in adjacencies:
            neighbor = adj["id"]
            if mode == 0:
                weight = adj["distance"]
            else :
                distance=adj["distance"]
                congestion=adj["congestion"]
                weight = distance/congestion
            dist[now][neighbor] = weight
            dist[neighbor][now] = weight

    # floyd
    for k in range(1, n):
        for i in range(1, n):
            for j in range(1, n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    path[i][j] = k

    # 求中间必经点的全排列
    k = len(nodes)
    nodes.sort()
    mindis = inf
    for i in permutations(nodes):
        # 计算每一种排列对应的最短路径
        distance = dist[start][nodes[0]]
        if dist[start][nodes[0]] == inf:
            return inf + 1
        for i in range(0, k - 2):
            if dist[nodes[i]][nodes[i + 1] == inf]:
                return inf + 1
            distance += dist[nodes[i]][nodes[i + 1]]
        if dist[nodes[k - 1]][1] == inf:
            return inf + 1
        distance += dist[nodes[k - 1]][start]

        if mindis > distance:
            mindis = distance
            anspath = []
            # 存储最短路径
            anspath.append(start)
            getpath(start, nodes[0])
            for i in range(0, k - 2):
                anspath.append(nodes[i])
                getpath(nodes[i], nodes[i + 1])
            anspath.append(nodes[k - 1])
            getpath(nodes[k - 1], start)
            anspath.append(start)

    return anspath
