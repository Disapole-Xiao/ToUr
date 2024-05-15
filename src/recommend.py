## 游学地推荐排序模块 ##

# 游学地模型定义已经更改至 travel/models.py
import os
import sys

# 设置 Django 项目根目录的路径
project_path = 'D:/MESS/Codes/ToUr'
sys.path.append(project_path)

# 设置 Django 项目的设置模块
os.environ['DJANGO_SETTINGS_MODULE'] = 'ToUr.settings'

# 初始化 Django
import django
django.setup()
# 现在可以导入 travel 应用的模型
from travel.models import Destination

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
        if bm(dest.name, input) != -1:
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

# # 根据li中每一项的属性attr排序，默认降序
def sort(li: list, attr: str, reverse=False, len=10, conti=False) -> list :
    # 重新建堆
    if conti == False:
        sorted1_data = Heapsort(li, attr, reverse)
        sorted2_data = sorted1_data[-10:]
        global sorted3_data 
        sorted3_data = sorted2_data[::-1]
        return sorted3_data

# 根据attr构建一个最大堆
def maxHeapify(h, start, end, attr):
    son = start * 2  # 左节点
    while son <= end:  # 如果左子树存在
        # 取左子树根和右子树根 两者中大者的下标
        if son + 1 <= end and getattr(h[son + 1], attr) > h[son][attr]:
            son += 1
        # 如果子节点的值大于根节点，则将根节点和子节点交换。即下沉操作
        if h[son][attr] > getattr(h[start], attr):
            h[start], h[son] = h[son], h[start]
            # 对子节点迭代执行相同的操作
            start, son = son, son * 2
        else:  # 如果子节点的值小于等于根节点,说明堆已经构造好了，退出循环
            break

# 根据attr构建一个最小堆
def minHeapify(h, start, end, attr):
    son = start * 2  # 左节点
    while son <= end:  # 如果左子树存在
        # 取左子树根和右子树根 两者中小者的下标
        if son + 1 <= end and getattr(h[son + 1], attr) < getattr(h[son], attr):
            son += 1
        # 如果子节点的值小于根节点，则将根节点和子节点交换。即下沉操作
        if getattr(h[son], attr) < getattr(h[start], attr):
            h[start], h[son] = h[son], h[start]
            # 对子节点迭代执行相同的操作
            start, son = son, son * 2
        else:  # 如果子节点的值大于等于根节点,说明堆已经构造好了，退出循环
            break

def Heapsort(arr, attr, reverse):
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





# 测试代码，数据来源maplist
if __name__ == "__main__":
    dests =list(Destination.objects.all()) 
    
    filtered_data = name_filter(dests,"大学")
    print('---- name filter ----')
    for i in filtered_data:
        print(i)

    sorted_data = sort(dests,"popularity",0,10)
    print('-----------')
    for i in sorted_data:
        print(i, i.popularity)
    
    sorted_data = sort(dests,"popularity",0,10)
    print('-----------')
    for i in sorted_data:
        print(i, i.popularity)