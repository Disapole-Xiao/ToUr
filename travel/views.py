from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
import json, bisect

from .models import Destination, Category, AmenityType, RestaurantType
from diary.models import Diary
from .funcs import distance
from src.routing import route_sgl, route_mul
from src.recommend import attr_sort, str_filter, tag_filter, type_filter

def index(request):
    ''' 首页，根据搜索词、筛选、排序选择器返回展示的游学地'''
    dests = list(Destination.objects.all())
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '热度最高')
    category = request.GET.get('category', '所有类别')
    # 搜索框不为空，按名字筛选
    if search != '':
        dests = str_filter(dests, lambda x: x.name, search)
    print('search:', *dests, sep='\n')
    # 类别筛选
    if category != '所有类别':
        dests = tag_filter(dests, lambda x: x.tags.all(), Category.objects.get(name=category))
    print('tag:', *dests, sep='\n')
    # 排序
    attr = 'popularity'
    if sort == '热度最高':
        attr = 'popularity'
    elif sort == '评分最高':
        attr = 'rating' 
    dests = attr_sort(dests, lambda x: getattr(x, attr), len=8)
    print('sort:', *dests, sep='\n')

    tags = Category.objects.all()
    tags = [tag.name for tag in tags]
    print(tags)

    context = {
        'dests': dests,
        'category': category,
        'search': search,
        'sort': sort,
        'tags': tags,
    }
    
    return render(request, 'travel/index.html', context)

def detail(request, dest_id):
    ''' 游学地详细界面 '''
    dest = get_object_or_404(Destination, pk=dest_id)
    related_diaries = Diary.objects.filter(location=dest).order_by('-rating')
    context = {
        'dest': dest,
        'related_diaries': related_diaries,
    }
    return render(request, 'travel/detail.html', context)
def map(request, dest_id):
    dest = get_object_or_404(Destination, pk=dest_id)

    restaurant_types = [x.name for x in RestaurantType.objects.all()]
    amenity_types = [x.name for x in AmenityType.objects.all()]

    context = {
        'dest': dest,
        'restaurant_types': restaurant_types,
        'amenity_types': amenity_types,
    }
    return render(request, 'travel/map.html', context)

def plan_route(request, dest_id):
    dest = get_object_or_404(Destination, pk=dest_id)
    map = json.loads(dest.mapjson)
    if request.method == 'POST':
        # 从请求体中获取 JSON 数据
        data = json.loads(request.body)
        selected_attractions = data.get('selected_attractions')
        selected_attractions = [int(attr_id) if attr_id != None else None for attr_id in selected_attractions]
        mode = data.get('mode')
        
        node_ids = []
        # 将 attractions 映射到 node
        if selected_attractions[0] == None:
            node_ids.append(map['entrance']) # 添加入口
        node_ids += [map['attractions'][attr_id]['entr_point'][0] for attr_id in selected_attractions if attr_id != None]
        print('node_ids = ',node_ids)
        # 调用路径规划算法
        if len(node_ids) == 2:
            planned_node_ids = route_sgl(map, node_ids[0], node_ids[1], mode)
        elif len(node_ids) > 2:
            planned_node_ids = route_mul(map, node_ids[1:], node_ids[0], mode)

        # 由node_id获得经纬度序列 [[lat2,lon1], [lat2,lon2], ...]
        lat_lon_seq = [[map['nodes'][id]['lat'], map['nodes'][id]['lon']] for id in planned_node_ids]
        
        return JsonResponse({'latLonSeq': lat_lon_seq})
    
def search_amenity(request, dest_id):
    ''' 返回选中景点附近的设施 '''
    dest = get_object_or_404(Destination, pk=dest_id)
    map = json.loads(dest.mapjson)
    
    attr_id = int(request.GET.get('id'))
    attr_type = request.GET.get('type', '')

    selected_attractions = map['attractions'][attr_id] # 在map找到对应景点
    amenities = map['amenities'] # 所有设施

    # 类别筛选
    if attr_type != '':
        amenities = type_filter(amenities, lambda x: x['type'], attr_type)
    # 计算距离，得到元组列表(distance, amenity)
    tuples = [(distance(
            x['coordinate']['lat'],
            x['coordinate']['lon'],
            selected_attractions['coordinate']['lat'],
            selected_attractions['coordinate']['lon']
            ), x) for x in amenities]
    # 排序
    amenities = attr_sort(tuples, lambda x: x[0], reverse=True)
    # 取距离 < AMENITY_SEARCH_RADIUS 的
    distances, amenities = zip(*amenities)
    r = bisect.bisect_right(distances, settings.AMENITY_SEARCH_RADIUS)

    return JsonResponse({'amenities': amenities[:r], 'distances': distances[:r]})