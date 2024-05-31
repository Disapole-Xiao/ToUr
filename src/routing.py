from itertools import permutations
from django.conf import settings
import json
import time
import csv

inf = float("inf")


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
            neighbor = adj["id"]
            distance = adj["distance"]
            congestion = adj["congestion"]
            weight = distance / congestion
            adj_list[node["id"]].append((neighbor, weight))

    return adj_list


# 返回值是id序列
def route_sgl(cur_map: dict, start: int, end: int, mode: str) -> list:
    # 从 Map 中获取边存储到邻接表 adj_list 中
    if mode == "distance":
        adj_list = adjlist_distance(cur_map["nodes"])
    elif mode == "time":
        adj_list = adjlist_time(cur_map["nodes"])

    # dijkstra
    M = len(adj_list)
    dist = [inf] * M
    visit = [1] * M
    path = [-1] * M
    dist[start] = 0
    visit[start] = 0
    temp = start

    while start != end:
        Min = inf
        for neighbor, weight in adj_list[start]:
            if dist[start] + weight < dist[neighbor]:
                dist[neighbor] = dist[start] + weight
                path[neighbor] = start
        for i in range(0, M):
            if visit[i] and dist[i] < Min:
                Min = dist[i]
                Next = i
        if Min == inf:
            print("No")
            break
        start = Next
        visit[start] = 0

    # 获取最短路径
    shortestPath = []
    # print("visit:", [x[0] for x in enumerate(visit) if x[1] == 0])
    # print("path:", {x[0]: x[1] for x in enumerate(path) if x[1] != -1})
    shortestPath.append(end)
    while end != temp:
        shortestPath.append(path[end])
        end = path[end]
    shortestPath.reverse()
    return shortestPath


# -------------------------


def getpath(a, b, path, anspath, idx):
    if path[a][b] == -1:
        return
    else:
        k = path[a][b]
        getpath(a, k, path, anspath, idx)
        # anspath[idx] = k
        anspath.append(k)
        # print(a,b,anspath)
        idx += 1
        getpath(k, b, path, anspath, idx)


def route_mul(cur_map: dict, nodes: list, start: int, mode: str) -> list:
    # 获取所需数据：dist矩阵，存储任意两点间的距离
    # n = len(cur_map["nodes"])
    # dist = [[inf for _ in range(0, n)] for _ in range(0, n)]
    # path = [[-1 for _ in range(0, n)] for _ in range(0, n)]
    # compute_nodes = cur_map["nodes"]
    # for node in compute_nodes:
    #     adjacencies = node["adj"]
    #     now = node["id"]
    #     for adj in adjacencies:
    #         neighbor = adj["id"]
    #         if mode == "distance":
    #             weight = adj["distance"]
    #         elif mode == "time":
    #             distance = adj["distance"]
    #             congestion = adj["congestion"]
    #             weight = distance / congestion
    #         dist[now][neighbor] = weight
    #         dist[neighbor][now] = weight

    start_time = time.time()
    
    # floyd
    # for k in range(0, n):
    #     for i in range(0, n):
    #         for j in range(0, n):
    #             if dist[i][j] > dist[i][k] + dist[k][j]:
    #                 dist[i][j] = dist[i][k] + dist[k][j]
    #                 path[i][j] = k
    # write_dist_to_file(dist, "src/dist1.csv")
    # write_path_to_file(path, "src/path1.csv")
    id=cur_map["id"]
    dictfilename="src/map/dist"+str(id)+"_"+mode+".csv"
    pathfilename="src/map/path"+str(id)+"_"+mode+".csv"
    dist = read_dist_from_file(dictfilename)
    path = read_path_from_file(pathfilename)
    end_time = time.time()
    execution_time = end_time - start_time
    print(execution_time)
    # 求中间必经点的全排列
    k = len(nodes)
    nodes.sort()
    mindis = inf
    anspath = []
    for per in permutations(nodes):
        # 计算每一种排列对应的最短路径
        distance = dist[start][per[0]]
        if dist[start][per[0]] == inf:
            continue
        for i in range(0, k - 2):
            if dist[per[i]][per[i + 1] == inf]:
                continue
            distance += dist[per[i]][per[i + 1]]
        if dist[per[k - 1]][start] == inf:
            continue
        distance += dist[per[k - 1]][start]
        
        if mindis > distance:
            mindis = distance
            anspath = []
            idx = 0
            # 存储最短路径
            anspath.append(start)
            # anspath[idx] = start
            idx += 1
            getpath(start, per[0], path, anspath, idx)
            for i in range(0, k - 1):
                anspath.append(per[i])
                # anspath[idx] = nodes[i]
                idx += 1
                getpath(per[i], per[i + 1], path, anspath, idx)
            anspath.append(per[k - 1])
            # anspath[idx] = nodes[k - 1]
            idx += 1
            getpath(per[k - 1], start, path, anspath, idx)
            anspath.append(start)
            idx += 1

    return anspath

def write_dist_to_file(dist, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in dist:
            writer.writerow(row)

def write_path_to_file(path, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in path:
            writer.writerow(row)

def read_dist_from_file(filename):
    dist = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            dist.append([float(cell) for cell in row])
    return dist

def read_path_from_file(filename):
    path = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            path.append([int(cell) for cell in row])
    return path

# 测试代码
if __name__ == "__main__":
    with open("static/maps/2.json", "r", encoding="utf-8") as f:
        jsonstr = f.read()
    map = json.loads(jsonstr)
    # print(route_sgl(map, 538, 359, "distance"))
    # print(route_sgl(map, 538, 359, "time"))
    start_time = time.time()
    print(route_mul(map, [326,334,376,62], 342, "distance"))
    end_time = time.time()
    execution_time = end_time - start_time
    print(execution_time)

    # start_time = time.time()
    # print(simulated_annealing(map, [326,334,376,62], 342, "time",1000,0.95,0.1,1000))
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print(execution_time)
