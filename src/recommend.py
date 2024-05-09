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
    def compute_interest_match(self, interest: list):
        match_count = sum(tag in self.tags for tag in interest)
        self.interest_match = match_count / len(interest)

data = [
    {
        "id": 1,
        "name": "Destination 1",
        "tags": ["tag1", "tag2"],
        "popularity": 100,
        "rating": 4.5,
        "province": "Province 1",
        "city": "City 1",
        "description": "Description 1"
    },
    {
        "id": 2,
        "name": "Destination 2",
        "tags": ["tag3", "tag4"],
        "popularity": 200,
        "rating": 4.8,
        "province": "Province 2",
        "city": "City 2",
        "description": "Description 2"
    },
    {
        "id": 3,
        "name": "Destination 3",
        "tags": ["tag5", "tag4"],
        "popularity": 30,
        "rating": 8.8,
        "province": "Province 3",
        "city": "City 3",
        "description": "Description 3"
    },
    {
        "id": 4,
        "name": "Destination 4",
        "tags": ["tag6", "tag7"],
        "popularity": 150,
        "rating": 4.2,
        "province": "Province 4",
        "city": "City 4",
        "description": "Description 4"
    },
    {
        "id": 5,
        "name": "Destination 5",
        "tags": ["tag8", "tag9"],
        "popularity": 250,
        "rating": 4.9,
        "province": "Province 5",
        "city": "City 5",
        "description": "Description 5"
    },
    {
        "id": 6,
        "name": "Destination 6",
        "tags": ["tag10", "tag11"],
        "popularity": 80,
        "rating": 7.6,
        "province": "Province 6",
        "city": "City 6",
        "description": "Description 6"
    },
    {
        "id": 7,
        "name": "Destination 7",
        "tags": ["tag12", "tag13"],
        "popularity": 180,
        "rating": 6.3,
        "province": "Province 7",
        "city": "City 7",
        "description": "Description 7"
    },
    {
        "id": 8,
        "name": "Destination 8",
        "tags": ["tag14", "tag15"],
        "popularity": 120,
        "rating": 9.1,
        "province": "Province 8",
        "city": "City 8",
        "description": "Description 8"
    },
    {
        "id": 9,
        "name": "Destination 9",
        "tags": ["tag16", "tag17"],
        "popularity": 220,
        "rating": 5.7,
        "province": "Province 9",
        "city": "City 9",
        "description": "Description 9"
    },
    {
        "id": 10,
        "name": "Destination 10",
        "tags": ["tag18", "tag19"],
        "popularity": 50,
        "rating": 8.0,
        "province": "Province 10",
        "city": "City 10",
        "description": "Description 10"
    },
    {
        "id": 11,
        "name": "Destination 11",
        "tags": ["tag20", "tag21"],
        "popularity": 300,
        "rating": 9.5,
        "province": "Province 11",
        "city": "City 11",
        "description": "Description 11"
    },
    
    {
        "id": 13,
        "name": "Destination 13",
        "tags": ["tag24", "tag25"],
        "popularity": 170,
        "rating": 7.2,
        "province": "Province 13",
        "city": "City 13",
        "description": "Description 13"
    },
    {
        "id": 14,
        "name": "Destination 14",
        "tags": ["tag26", "tag27"],
        "popularity": 350,
        "rating": 9.8,
        "province": "Province 14",
        "city": "City 14",
        "description": "Description 14"
    },
    {
        "id": 15,
        "name": "Destination 15",
        "tags": ["tag28", "tag29"],
        "popularity": 90,
        "rating": 5.4,
        "province": "Province 15",
        "city": "City 15",
        "description": "Description 15"
    },
    {
        "id": 16,
        "name": "Destination 11",
        "tags": ["tag20", "tag21"],
        "popularity": 301,
        "rating": 9.2,
        "province": "Province 11",
        "city": "City 11",
        "description": "Description 11"
    },
    
    {
        "id": 17,
        "name": "Destination 13",
        "tags": ["tag24", "tag25"],
        "popularity": 17,
        "rating": 7.2,
        "province": "Province 13",
        "city": "City 13",
        "description": "Description 13"
    },
    {
        "id": 18,
        "name": "Destination 14",
        "tags": ["tag26", "tag27"],
        "popularity": 359,
        "rating": 9.9,
        "province": "Province 14",
        "city": "City 14",
        "description": "Description 14"
    },
    {
        "id": 19,
        "name": "Destination 19",
        "tags": ["tag28", "tag29"],
        "popularity": 900,
        "rating": 5.9,
        "province": "Province 19",
        "city": "City 15",
        "description": "Description 15"
    }
]


## ------- 筛选接口定义---------

# BM 匹配算法
def bm(T: str, p: str) -> int:
    n, m = len(T), len(p)
    
    bc_table = generateBadCharTable(p)              # 生成坏字符位置表
    gs_list = generageGoodSuffixList(p)             # 生成好后缀规则后移位数表
    
    i = 0
    while i <= n - m:
        j = m - 1
        while j > -1 and T[i + j] == p[j]:          # 进行后缀匹配，跳出循环说明出现坏字符
            j -= 1
        if j < 0:
            return i                                # 匹配完成，返回模式串 p 在文本串 T 中的位置
        bad_move = j - bc_table.get(T[i + j], -1)   # 坏字符规则下的后移位数
        good_move = gs_list[j]                      # 好后缀规则下的后移位数
        i += max(bad_move, good_move)               # 取两种规则下后移位数的最大值进行移动
    return -1
            
    
# 生成坏字符位置表
# bc_table[bad_char] 表示坏字符在模式串中最后一次出现的位置
def generateBadCharTable(p: str):
    bc_table = dict()
    
    for i in range(len(p)):
        bc_table[p[i]] = i                          # 更新坏字符在模式串中最后一次出现的位置
    return bc_table

# 生成好后缀规则后移位数表
# gs_list[j] 表示在 j 下标处遇到坏字符时，可根据好规则向右移动的距离
def generageGoodSuffixList(p: str):
    # 好后缀规则后移位数表
    # 情况 1: 模式串中有子串匹配上好后缀
    # 情况 2: 模式串中无子串匹配上好后缀，但有最长前缀匹配好后缀的后缀
    # 情况 3: 模式串中无子串匹配上好后缀，也找不到前缀匹配
    
    m = len(p)
    gs_list = [m for _ in range(m)]                 # 情况 3：初始化时假设全部为情况 3
    suffix = generageSuffixArray(p)                 # 生成 suffix 数组
    
    j = 0                                           # j 为好后缀前的坏字符位置
    for i in range(m - 1, -1, -1):                  # 情况 2：从最长的前缀开始检索
        if suffix[i] == i + 1:                      # 匹配到前缀，即 p[0...i] == p[m-1-i...m-1]
            while j < m - 1 - i:
                if gs_list[j] == m:
                    gs_list[j] = m - 1 - i          # 更新在 j 处遇到坏字符可向后移动位数
                j += 1
        
    for i in range(m - 1):                          # 情况 1：匹配到子串 p[i-s...i] == p[m-1-s, m-1]
        gs_list[m - 1 - suffix[i]] = m - 1 - i      # 更新在好后缀的左端点处遇到坏字符可向后移动位数
    return gs_list

# 生成 suffix 数组
# suffix[i] 表示为以下标 i 为结尾的子串与模式串后缀匹配的最大长度
def generageSuffixArray(p: str):
    m = len(p)
    suffix = [m for _ in range(m)]                  # 初始化时假设匹配的最大长度为 m
    for i in range(m - 2, -1, -1):                  # 子串末尾从 m - 2 开始
        start = i                                   # start 为子串开始位置
        while start >= 0 and p[start] == p[m - 1 - i + start]:
            start -= 1                              # 进行后缀匹配，start 为匹配到的子串开始位置
        suffix[i] = i - start                       # 更新以下标 i 为结尾的子串与模式串后缀匹配的最大长度
    return suffix



# 模式串：input
# 目标串：所有dest.name
# 通过景点名称筛选，符合条件将整个景点加入返回列表
def name_filter(li: list, input: str) -> list :
    over_destinations = []
    for dest in li:
        if bm(input,dest.name)!= 0:
            over_destinations.append(dest)
    
    return over_destinations


# 每一个元素的属性attr（数组）中是否包含val
def tag_filter(li: list, attr: str, val: str) -> list :
    tag_destinations = []
    for dest in li:
        if val in attr:
            tag_destinations.append(dest)
    return tag_destinations

# li中的每一项的属性attr是否与type相等。getattr函数
# 例如type_filter(amenities, "type", "厕所")，返回amenities数组中符合属性type的值为“厕所"的项
def type_filter(li: list, attr: str, val: str) -> list :
    type_filtered = []
    for dest in li:
        if(bm(val,dest.type)!=0):
            type_filtered.append(dest)
    return type_filtered


# ------- 排序---------
# 全局变量存堆
h = []

# # 根据li中每一项的属性attr排序
def sort(li: list, attr: str,  reverse=False, len=10) -> list :

        sorted1_data = Heapsort(li,attr,reverse)
        sorted2_data = sorted1_data[-10:]
        global sorted3_data 
        sorted3_data = sorted2_data[::-1]
        return sorted3_data






def maxHeapify(h, start, end, attr):
    son = start * 2  # 左节点
    while son <= end:  # 如果左子树存在
        # 取左子树根和右子树根 两者中大者的下标
        if son + 1 <= end and h[son + 1][attr] > h[son][attr]:
            son += 1
        # 如果子节点的值大于根节点，则将根节点和子节点交换。即下沉操作
        if h[son][attr] > h[start][attr]:
            h[start], h[son] = h[son], h[start]
            # 对子节点迭代执行相同的操作
            start, son = son, son * 2
        else:  # 如果子节点的值小于等于根节点,说明堆已经构造好了，退出循环
            break

def minHeapify(h, start, end, attr):
    son = start * 2  # 左节点
    while son <= end:  # 如果左子树存在
        # 取左子树根和右子树根 两者中小者的下标
        if son + 1 <= end and h[son + 1][attr] < h[son][attr]:
            son += 1
        # 如果子节点的值小于根节点，则将根节点和子节点交换。即下沉操作
        if h[son][attr] < h[start][attr]:
            h[start], h[son] = h[son], h[start]
            # 对子节点迭代执行相同的操作
            start, son = son, son * 2
        else:  # 如果子节点的值大于等于根节点,说明堆已经构造好了，退出循环
            break

def Heapsort(arr, attr,reverse):
    h = [None] + arr  # 这里是因为列表从0开始计数，而我们找的子节点父节点的关系是2倍或2倍+1
    result = []
    root = 1  # 堆顶下标
    count = len(h)  # 获取堆元素个数
    for i in range(count // 2, root - 1, -1):  # 逆序枚举列表的元素
        # 自底向上地构造堆
        if reverse == False:
            minHeapify(h, i, count - 1, attr)
        else:
            maxHeapify(h, i, count - 1, attr)
    
    for i in range(count-1, 0, -1): 
            result.append(h[root])
            h[i], h[root] = [None], h[i]  # 保持除最后一个元素以外整个堆的合法性
            # 保持除最后第二个元素以外整个堆的合法性
            if reverse == False:
                minHeapify(h, root, i - 1, attr)
            else:
                maxHeapify(h, root, i - 1, attr)
    return result[1:]  # 返回排好序的元素



# sorted1_data = Heapsort(data, "popularity",0)
# sorted2_data = sorted1_data[-10:]
# sorted3_data = sorted2_data[::-1]
# print(sorted3_data)
# print(data[0]["name"])
# print(Heapsort(data,"popularity"))
# # print(data)

sorted_data = sort(data,"popularity",0,10)
print(sorted_data)





# 测试代码，数据来源maplist
# if __name__ == "__main__":
#     with open(f"data/maplist.json", 'r',encoding="utf-8") as fp:
#         destinations = json.load(fp)
#     destinations = [Destination(dest) for dest in destinations] # 数组，每一项为Destination对象