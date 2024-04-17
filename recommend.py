import sys

class Map:
    def __init__(self):
        self.destinations = destinations #景点数量
        self.lines = lines  #道路数量
        self.diaries = diaries  #日记数量
        self.world = [0 for _ in range(200) for _ in range (200)]   #创建一个200x200的数组存储
        
    # 根据名称/关键词（keyword）、类别（type）筛选目的地
    def dest_search(maplist: dict, type=None, keyword=None) 

    # 根据热度（sort=1）、评分（sort=2）、综合（sort=0）排序目的地，page第几页
    def dest_sort(maplist: dict, interests: list, sort=0, page) 

    # 单目标 mode=0 最短距离策略 mode=1 最短时间策略
    def route_sgl(cur_map: Map, start: int, end: int, mode=0|1) 

    # 多目标 nodes是需要经过的点的坐标数组
    def route_mul(cur_map: Map, nodes: list, start:int, mode=0|1) 

class user:
    def __init__(self):
        self.id = id  #用户名

class Destination:
    def __init__(self):
        self.name = name    #景点名称
        self.category = category    #分类
        self.keywords = keywords    #关键词
        self.popularity = popularity    #热度
        self.rating = rating    #评分


#destinations为list name——景区名称 category——分类 keywords——关键词 
#查找算法 way——方式 1-3分别代表从name到keywords为参数进行查找

def choose_destinations(destinations, name, category, keywords, way)：
    chooseed_destinations = [] #存放查找完成后的list

    if way == 1:
        key = name
    elif way == 2:
        key = category
    elif way == 3:
        key = keywords
    

    for dest in destinations:       # 筛选查找出符合要求的景点
        if key in dest.keywords:
                filtered_destinations.append(dest)
    
    return filtered_destinations


#destinations为list popularity——热度 rating——评分 interests——兴趣
#排序算法 sort——排序方式

#返回中枢值位置
def partition(destinations, low, high, key):
    i = low - 1
    pivot = getattr(destinations[high], key)

    for j in range(low, high):
        if getattr(destinations[j], key) <= pivot:
            i += 1
            destinations[i], destinations[j] = destinations[j], destinations[i]
    
    destinations[i + 1], destinations[high] = destinations[high], destinations[i + 1]
    return i + 1

#进行快速排序
def quicksort(destinations, low, high, key):
    if low < high:
        pi = partition(destinations, low, high, key)
        quicksort(destinations, low, pi - 1, key)
        quicksort(destinations, pi + 1, high, key)

#对外接口，进行排序的根据选择
def sort_destinations(destinations, sort):
    if sort == 1:
        key = 'popularity'
    elif sort == 2:
        key = 'rating'
    elif sort == 3:
        key = 'interests'
    else:
        print("Invalid sort parameter. Please choose 1 for popularity, 2 for rating, or 3 for interests.")
        return
    
    quicksort(destinations, 0, len(destinations) - 1, key)
    return destinations[:10]

# 创建一些 Destination 实例
dest1 = Destination("Destination1", 100, 4.5, 200)
dest2 = Destination("Destination2", 200, 4.8, 150)
dest3 = Destination("Destination3", 150, 4.2, 180)
dest4 = Destination("Destination4", 180, 4.6, 220)

# 创建 Destination 对象列表
destinations = [dest1, dest2, dest3, dest4]

# 输出前十个排序后的目的地信息
for dest in sorted_destinations:
    print(dest.name, dest.popularity, dest.rating, dest.interests)

# 示例用法
dest1 = Destination("景点1", "自然风光", ["自然", "湖泊"], 1000, 4.5)
dest2 = Destination("景点2", "历史遗迹", ["古代", "文明"], 800, 4.0)
dest3 = Destination("景点3", "现代建筑", ["摩天大楼", "城市"], 1200, 4.8)

d
# Sample destinations data

destinations = [
    Destination("Great Wall", "Historical", ["history", "culture"], 95, 4.5),
    Destination("Eiffel Tower", "Landmark", ["architecture", "view"], 90, 4.3),
    Destination("Grand Canyon", "Natural", ["nature", "scenery"], 88, 4.4),
    Destination("Harvard University", "Education", ["university", "history"], 92, 4.6),
    Destination("Oxford University", "Education", ["college", "study"], 89, 4.5),
    Destination("Disneyland", "Entertainment", ["theme park", "fun"], 94, 4.7),
    Destination("Louvre Museum", "Art", ["art", "painting"], 91, 4.4),
]

