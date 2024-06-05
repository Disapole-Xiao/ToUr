import os, sys, json, time, math, random
from itertools import permutations

# 设置 Django 项目根目录的路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)

# 设置 Django 项目的设置模块
os.environ['DJANGO_SETTINGS_MODULE'] = 'ToUr.settings'

# 初始化 Django
import django
from django.conf import settings
from django.core.cache import cache
django.setup()


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

    WALKING_SPEED = settings.WALKING_SPEED
    BICYCLE_SPEED = settings.BICYCLE_SPEED
    MOTORBIKE_SPEED = settings.MOTORBIKE_SPEED
    for node in nodes:
        adjacencies = node["adj"]
        for adj in adjacencies:
            neighbor = adj["id"]
            distance = adj["distance"]
            congestion = adj["congestion"]
            if(adj["motorbike"]==True):
                speed=MOTORBIKE_SPEED
            elif(adj["bicycle"]==True):
                speed=BICYCLE_SPEED
            else:
                speed=WALKING_SPEED
            weight = distance*speed / congestion
            adj_list[node["id"]].append((neighbor, weight))

    return adj_list

def route_sgl(cur_map: dict, start: int, end: int, mode: str):  
    # 从 Map 中获取边存储到邻接表 adj_list 中
    if mode == "distance":
        adj_list = adjlist_distance(cur_map["nodes"])
    elif mode == "time":
        adj_list = adjlist_time(cur_map["nodes"])

    # route_sgl
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
            print("路径不存在")
            return None, None
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
    return shortestPath,Min


# -------------------------

initial_temp = 10
cooling_rate = 0.9
def calculate_distance(per,cur_map,start,mode,k):
    anspath=[]
    result=route_sgl(cur_map, start, per[0], mode)
    anspath+=result[0]
    distance=result[1]
    for i in range(0, k - 1):
        result=route_sgl(cur_map, per[i], per[i + 1], mode)
        tem=result[1]
        anspath+=result[0]
        distance += tem
    result=route_sgl(cur_map, per[k - 1], start, mode)
    tem=result[1]
    anspath+=result[0]
    distance += tem
    return distance,anspath

def perturb_route(route):
    """通过交换两点的位置来扰动当前路径"""
    idx1, idx2 = random.sample(range(0, len(route)), 2)  # 选择两个不同的点（不包括起点）
    route[idx1], route[idx2] = route[idx2], route[idx1]
    return route


def route_mul(cur_map: dict, nodes: list, start: int, mode: str) -> list:
    k = len(nodes)
    if k>=5:
    # 模拟退火算法主函数
        nodes.sort()
        mindis = inf
        current_route = nodes
        result=calculate_distance(current_route,cur_map,start,mode,k)
        current_cost = result[0]
        anspath=result[1]
        temperature = initial_temp

        while temperature > 1:
            new_route = perturb_route(current_route.copy())
            result=calculate_distance(new_route,cur_map,start,mode,k)
            new_cost = result[0]
            
            if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / temperature):
                current_route = new_route
                current_cost = new_cost
                anspath=result[1]
                order=new_route

            temperature *= cooling_rate
        order=[start]+order+[start]
        return anspath,current_cost,order
    else:
        nodes.sort()
        mindis = inf
        anspath = []
        for per in permutations(nodes):
            # 计算每一种排列对应的最短路径
            anspath=[]
            result=route_sgl(cur_map, start, per[0], mode)
            anspath+=result[0]
            distance=result[1]
            for i in range(0, k - 1):
                result=route_sgl(cur_map, per[i], per[i + 1], mode)
                tem=result[1]
                anspath+=result[0]
                distance += tem
            result=route_sgl(cur_map, per[k - 1], start, mode)
            tem=result[1]
            anspath+=result[0]
            distance += tem
            
            if mindis > distance:
                order=per
                mindis = distance
                finalanspath = anspath.copy()
        order=[start]+order+[start]
        return finalanspath,mindis,order

# 测试代码
if __name__ == "__main__":
    with open("static/maps/3.json", "r", encoding="utf-8") as f:
        jsonstr = f.read()
    map = json.loads(jsonstr)
    start_time = time.time()
    mode = "distance"
    # 单目标
    # planned_node_ids, cost = route_sgl(map, 538, 359, mode)
    # print('道路点序列', planned_node_ids)
    # print('cost', cost, 'm' if mode=="distance" else 's')

    # 多目标
    # planned_node_ids, cost, entr_point_order = route_mul(map, [326,334,376,62,436,333], 342, "distance")
    # print('道路点序列', planned_node_ids)
    # print('cost', cost, 'm' if mode=="distance" else 's')
    # print('入口点顺序', entr_point_order)

    # map_json, map_id = cache.get('map_json')
    end_time = time.time()
    execution_time = end_time - start_time
    print('执行时间', execution_time)

    # start_time = time.time()
    # print(simulated_annealing(map, [326,334,376,62], 342, "time",1000,0.95,0.1,1000))
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print(execution_time)
