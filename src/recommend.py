''' 游学地推荐排序模块 '''
import os
import sys

# 设置 Django 项目根目录的路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)

# 设置 Django 项目的设置模块
os.environ['DJANGO_SETTINGS_MODULE'] = 'ToUr.settings'

# 初始化 Django
import django
django.setup()

# 导入你的模型
from travel.models import Category, Destination
from django.core.cache import cache

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


from typing import Callable
# 模式串：input
# 目标串：所有dest.name 
# 通过字符串匹配筛选，符合条件将整个景点加入返回列表 f应该返回一个字符串
def str_filter(li: list, f, str: str) -> list :
    str_filtered = []
    for item in li:
        attr = f(item)
        if bm(attr, str) != -1:
            str_filtered.append(item)
    
    return str_filtered


# f返回attr，每一个元素的属性attr（数组）中是否包含tag。Destination
def tag_filter(li: list, f, tag: str) -> list :
    tag_filtered = []
    for item in li:
        tags = f(item)
        if tag in tags:
            tag_filtered.append(item)
    return tag_filtered

# f返回item的类型，是否与type相等。
# 例如type_filter(amenities, lambda x:x["type"], "厕所")，返回amenities数组中符合属性type的值为"厕所"的项
def type_filter(li: list, f, type: str) -> list :
    type_filtered = []
    for item in li:
        if(f(item) == type):
            type_filtered.append(item)
    return type_filtered


# ------- 排序---------
def attr_sort(li, f, arr_name, ascend=False, l=None, conti=False):
    ''' 不完全堆排。f返回attr，根据li中每一项的属性attr排序，默认降序。conti=True时，继续上次排序，否则重新排序。 '''
    cache_key = f'{arr_name}_heap'
    if l is None:
        l = len(li)
    
    if not conti:
        # 创建一个新的堆
        heap = build_heap(li, f, ascend)
        heap_end = len(heap)-1
        # 在堆上执行局部排序
        sorted_count = partial_heapsort(heap, f, l, ascend, heap_end)
        # 缓存堆和实际排序的元素数量
        cache.set(cache_key, (heap, sorted_count))
        sorted_part = heap[:-sorted_count-1:-1]  # 获取排序部分
    else:
        # 从缓存获取之前的堆和已排序元素的数量
        heap, prev_sorted_count = cache.get(cache_key)
        heap_end = len(heap) -1 - prev_sorted_count
        # 继续堆排序，从上次结束的位置开始
        additional_sorted_count = partial_heapsort(heap, f, l, ascend, heap_end)
        # 更新缓存的排序进度
        cache.set(cache_key, (heap, prev_sorted_count + additional_sorted_count))
        sorted_part = heap[-prev_sorted_count-1:-(prev_sorted_count + additional_sorted_count+1):-1]  # 获取排序部分
    return sorted_part

def build_heap(li, f, ascend):
    ''' 建堆 ascend=False 大根堆 '''
    heap = [None] + li  # 使用 1-based index
    heap_end = len(heap) - 1

    # 自底向上构造堆
    for i in range(heap_end // 2, 0, -1):
        heapify(heap, i, heap_end, f, ascend)

    return heap

def partial_heapsort(h, f, l, ascend, heap_end):
    ''' pop出最多l个元素放于堆末尾（实际已不属于堆）返回实际排序元素数量 '''
    limit = min(heap_end, l)  # 计算实际的操作上限

    # 只进行实际可进行次数的选择堆顶元素的操作
    for end in range(heap_end, heap_end - limit, -1):
        h[1], h[end] = h[end], h[1]  # 交换堆顶和堆的最后一个元素
        heapify(h, 1, end - 1, f, ascend)  # 重新调整堆

    return limit  # 返回排序的结果和实际排序的元素数量

def heapify(h, parent, heap_end, f, ascend):
    ''' 堆调整 ascend=False 大根堆 '''
    son = parent * 2 # 左子
    while son <= heap_end:
        # 小根堆选择孩子中的较小者，大跟堆选择孩子中较大者
        if son + 1 <= heap_end and ((f(h[son + 1]) < f(h[son])) if ascend else (f(h[son + 1]) > f(h[son]))):
            son += 1
        # 交换父子
        if (f(h[son]) < f(h[parent]) if ascend else f(h[son]) > f(h[parent])):
            h[parent], h[son] = h[son], h[parent]
            parent = son
            son = parent * 2
        else:
            break


# 测试代码，数据来源数据库
if __name__ == "__main__":
    dests =list(Destination.objects.all()) 
    
    # filtered_data = str_filter(dests, lambda x:x.name, "北京")
    # print('---- name filter ----')
    # for i in filtered_data:
    #     print(i)
    
    # filtered_data = tag_filter(dests, lambda x:x.tags.all(), Category.objects.get(name="学院高校"))
    # print('---- tag filter ----')
    # for i in filtered_data:
    #     print(i, i.tags.all())

    sorted_data = attr_sort(dests, lambda x:x.popularity, 'dests', l=8)
    print('----sort popularity-------')
    for i in sorted_data:
        print(i, i.popularity)
    print('---标准答案:', *Destination.objects.order_by('-popularity')[:8], sep='\n')
    
    sorted_data = attr_sort(dests, lambda x:x.rating, 'dests', l=10, ascend=True)
    print('----sort rating-------')
    for i in sorted_data:
        print(i, i.rating)
    print('---标准答案:', *Destination.objects.order_by('rating')[:10], sep='\n')

    sorted_data = attr_sort(dests, lambda x:x.rating, 'dests', l=8, ascend=True, conti=True)
    print('----sort rating conti-------')
    for i in sorted_data:
        print(i, i.rating)
    print('---标准答案:', *Destination.objects.order_by('rating')[10:18], sep='\n')