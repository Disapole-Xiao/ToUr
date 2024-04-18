## 游学地推荐排序模块 ##

import json

# 游学地，对应maplist中的一项
class Destination:
    def __init__(self, dic):
        self.id = dic["id"]    #id
        self.name = dic["name"]    #游学地名称
        self.tags = dic["tags"]    #关键词
        self.popularity = dic["popularity"]    #热度
        self.rating = dic["rating"]    #评分
        self.province = dic["province"] # 省
        self.city = dic["city"] # 市
        self.description = dic["description"] # 简介
        
        self.interest_match = 0 # 与用户的兴趣匹配度
    
    # 给定用户的兴趣标签，计算游学地与用户的兴趣匹配度
    def compute_interest_match(interest: list):
        pass


## ------- 筛选接口定义---------
def bm():
    pass

# 模式串：input
# 目标串：所有dest.name
# 通过景点名称筛选，符合条件将整个景点加入返回列表
def name_filter(li: list, input: str) -> list :
    pass

# 每一个dest.tags是否包含tag
def tag_filter(li: list, tag: str) -> list :
    pass

# li中的每一项的属性attr是否与type相等。getattr函数
# 例如type_filter(amenities, "type", "厕所")，返回amenities数组中符合属性type的值为“厕所"的项
def type_filter(li: list, attr: str, val: str) -> list :
    pass

## ------- 排序---------
# 全局变量存堆
h = []
# 根据li中每一项的属性attr排序
def sort(li: list, attr: str, conti=True, reverse=False, len=10) -> list :
    # 需要重新建堆，复制一份li，建堆，建堆时注意是否需要逆序
    if conti==False
    #原本的堆pop出len个
    else: 




#destinations为list name——景区名称 category——分类 keywords——关键词 
#查找算法 way——方式 1-3分别代表从name到keywords为参数进行查找

def choose_destinations(destinations, name,  keywords, way):
    chooseed_destinations = [] #存放查找完成后的list

    if way == 1:
        key = name
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




# 测试代码，数据来源maplist
if __name__ == "__main__":
    with open(f"data/maplist.json", 'r',encoding="utf-8") as fp:
        destinations = json.load(fp)
    destinations = [Destination(dest) for dest in destinations] # 数组，每一项为Destination对象
    # 没写完

