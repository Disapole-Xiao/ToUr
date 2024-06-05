import os, sys, json, time, math, random

# 设置 Django 项目根目录的路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)

# 设置 Django 项目的设置模块
os.environ['DJANGO_SETTINGS_MODULE'] = 'ToUr.settings'

# 初始化 Django
import django
from django.conf import settings
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


def adjlist_time(nodes,vehicle):
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
            if(adj["motorbike"]==True and vehicle=="motorbike"):
                speed=MOTORBIKE_SPEED
            elif(adj["bicycle"]==True and vehicle=="bicycle"):
                speed=BICYCLE_SPEED
            else:
                speed=WALKING_SPEED
            weight = distance / (speed * congestion)
            adj_list[node["id"]].append((neighbor, weight))

    return adj_list

def route_sgl(cur_map: dict, start: int, end: int, mode: str,vehicle=None):  
    # 从 Map 中获取边存储到邻接表 adj_list 中
    if mode == "distance":
        adj_list = adjlist_distance(cur_map["nodes"])
    elif mode == "time":
        adj_list = adjlist_time(cur_map["nodes"],vehicle)

    # route_sgl
    M = len(adj_list)
    dist = [inf] * M
    visit = [1] * M
    path = [-1] * M
    dist[start] = 0
    visit[start] = 0
    temp = start
    Min = 0
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
    return shortestPath, Min


# -------------------------

initial_temp = 10
cooling_rate = 0.9
def calculate_distance(per,cur_map,start,mode,k,vehicle):
    anspath=[]
    result=route_sgl(cur_map, start, per[0], mode,vehicle)
    anspath+=result[0]
    distance=result[1]
    for i in range(0, k - 1):
        result=route_sgl(cur_map, per[i], per[i + 1], mode,vehicle)
        tem=result[1]
        anspath+=result[0][1:]
        distance += tem
    result=route_sgl(cur_map, per[k - 1], start, mode,vehicle)
    tem=result[1]
    anspath+=result[0][1:]
    distance += tem
    return distance,anspath

def perturb_route(route):
    """通过交换两点的位置来扰动当前路径"""
    idx1, idx2 = random.sample(range(0, len(route)), 2)  # 选择两个不同的点（不包括起点）
    route[idx1], route[idx2] = route[idx2], route[idx1]
    return route

def isVisited(visited):
    return all(visited[1:])

def route_mul(cur_map: dict, nodes: list, start: int, mode: str,vehicle=None):
    N = len(nodes)
    if N>=20:
    # 模拟退火算法主函数
        nodes.sort()
        current_route = nodes
        result=calculate_distance(current_route,cur_map,start,mode,N,vehicle)
        current_cost = result[0]
        anspath=result[1]
        temperature = initial_temp
        order=current_route
        while temperature > 1:
            new_route = perturb_route(current_route.copy())
            result=calculate_distance(new_route,cur_map,start,mode,N,vehicle)
            new_cost = result[0]
            if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / temperature):
                current_route = new_route
                current_cost = new_cost
                anspath=result[1]
                order=new_route

            temperature *= cooling_rate
        order=[start]+list(order)+[start]
        return anspath,current_cost,order
    else:
        nodes=[start]+nodes
        N+=1
        M = 1 << (N - 1)
        dp = [[inf] * M for _ in range(N)]
        g = [[inf] * N for _ in range(N)]
        path = [[list] * N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                if i==j:
                    g[i][j]=0
                elif i<j:
                    result=route_sgl(cur_map, nodes[i], nodes[j], mode,vehicle)
                    g[i][j]=result[1]
                    path[i][j]=result[0]
                    g[j][i]=g[i][j]
                    path[j][i]=result[0][::-1]
        
        for i in range(N):
            dp[i][0] = g[i][0]


        # 求解dp[i][j],先跟新列在更新行
        for j in range(1, M):
            for i in range(N):
                dp[i][j] = inf
                # 如果集和j(或状态j)中包含结点i,则不符合条件退出
                if i > 0 and ((j >> (i - 1)) & 1) == 1:
                    continue
                for k in range(1, N):
                    if ((j >> (k - 1)) & 1) == 0:
                        continue
                    dp[i][j] = min(dp[i][j], g[i][k] + dp[k][j ^ (1 << (k - 1))])
        # 标记访问数组
        anspath = []
        final_anspath=[]
        visited = [False] * N
        # 前驱节点编号
        pioneer = 0
        min_dist = inf
        S = M - 1
        # 把起点结点编号加入容器
        anspath.append(0)
        final_anspath.append(nodes[0])
        while not isVisited(visited):
            for i in range(1, N):
                if not visited[i] and (S & (1 << (i - 1))) != 0:
                    if min_dist > g[i][pioneer] + dp[i][(S ^ (1 << (i - 1)))]:
                        min_dist = g[i][pioneer] + dp[i][(S ^ (1 << (i - 1)))]
                        temp = i
            pioneer = temp
            anspath.append(pioneer)
            final_anspath.append(nodes[pioneer])
            visited[pioneer] = True
            S = S ^ (1 << (pioneer - 1))
            min_dist = inf
        anspath.append(0)
        final_anspath.append(nodes[0])
        pioneer = 0
        final_path=[nodes[0]]
        for per in anspath[1:]:
            final_path+=path[pioneer][per][1:]
            pioneer=per
        return final_path,dp[0][M-1],final_anspath

# 测试代码
if __name__ == "__main__":
    with open("static/maps/4.json", "r", encoding="utf-8") as f:
        jsonstr = f.read()
    map = json.loads(jsonstr)
    start_time = time.time()
    mode = "time"
    # 单目标
    planned_node_ids, cost = route_sgl(map, 138, 34, mode, 'motorbike')
    print('道路点序列', planned_node_ids)
    print('cost', cost, 'm' if mode=="distance" else 's')

    # 多目标
    # start_time = time.time()
    # planned_node_ids, cost, entr_point_order = route_mul(map, [1316,137], 1310, mode,"bicycle")
    # print('道路点序列', planned_node_ids)
    # print('cost', cost, 'm' if mode=="distance" else 's')
    # print('入口点顺序', entr_point_order)

    # cache.set('test', map)
    end_time = time.time()
    execution_time = end_time - start_time
    print('执行时间', execution_time)

    # start_time = time.time()
    # print(simulated_annealing(map, [326,334,376,62], 342, "time",1000,0.95,0.1,1000))
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print(execution_time)
