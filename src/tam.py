import numpy as np
import math
import random

def calculate_distance(route, distance_matrix):
    """计算给定路线的总距离"""
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i + 1]]
    # 加上回到起点的距离
    total_distance += distance_matrix[route[-1]][route[0]]
    return total_distance

def generate_initial_solution(num_points, required_points):
    """生成一个包含所有必经点的初始解"""
    route = list(set(range(num_points)) - set(required_points))
    random.shuffle(route)
    # 在随机位置插入必经点
    for point in required_points:
        route.insert(random.randint(0, len(route)), point)
    route.insert(0, required_points[0])  # 假设必经点列表的第一个点是起点
    print(route)
    return route

def perturb_route(route):
    """通过交换两点的位置来扰动当前路径"""
    idx1, idx2 = random.sample(range(1, len(route)), 2)  # 选择两个不同的点（不包括起点）
    route[idx1], route[idx2] = route[idx2], route[idx1]
    return route

def simulated_annealing(distance_matrix, initial_temp, cooling_rate, num_points, required_points):
    """模拟退火算法主函数"""
    current_route = generate_initial_solution(num_points, required_points)
    current_cost = calculate_distance(current_route, distance_matrix)
    temperature = initial_temp

    while temperature > 1:
        new_route = perturb_route(current_route.copy())
        new_cost = calculate_distance(new_route, distance_matrix)
        
        if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / temperature):
            current_route = new_route
            current_cost = new_cost

        temperature *= cooling_rate

    return current_route, current_cost

# 假设数据
num_points = 500  # 总点数
required_points = [0, 100, 200, 300, 400, 499]  # 必经点
distance_matrix = np.random.randint(1, 100, size=(num_points, num_points))
np.fill_diagonal(distance_matrix, 0)

# 模拟退火参数
initial_temp = 10000
cooling_rate = 0.999

# 运行算法
best_route, best_cost = simulated_annealing(distance_matrix, initial_temp, cooling_rate, num_points, required_points)
print("Best route:", best_route)
print("Cost of the route:", best_cost)
