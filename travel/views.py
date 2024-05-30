from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
import json, bisect

from .models import Destination, Category, AmenityType, RestaurantType
from diary.models import Diary
from .funcs import distance, comprehensive_tuple
from src.routing import route_sgl, route_mul
from src.recommend import attr_sort, str_filter, tag_filter, type_filter

def index(request):
    ''' 首页，根据搜索词、筛选、排序选择器返回展示的游学地'''
    dests = list(Destination.objects.all())
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '综合排序')
    category = request.GET.get('category', '所有类别')
    # 搜索框不为空，按名字筛选
    if search != '':
        dests = str_filter(dests, lambda x: x.name, search)
    # print('----- str filter:', *dests, sep='\n')
    # 类别筛选
    if category != '所有类别':
        dests = tag_filter(dests, lambda x: x.tags.all(), Category.objects.get(name=category))
    # print('----- tag fliter:', *dests, sep='\n')
    # 排序
    if sort == '综合排序':
        dests = attr_sort(dests, lambda x: comprehensive_tuple(x, request.user), l=8)
    elif sort == '热度最高':
        dests = attr_sort(dests, lambda x: x.popularity, l=8)
    elif sort == '评分最高':
        dests = attr_sort(dests, lambda x: x.rating, l=8)
    # print('----- sort:', *dests, sep='\n')

    tags = Category.objects.all()
    tags = [tag.name for tag in tags]

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
def map(request, dest_id, edit=False):
    dest = get_object_or_404(Destination, pk=dest_id)

    restaurant_types = [x.name for x in RestaurantType.objects.all()]
    amenity_types = [x.name for x in AmenityType.objects.all()]

    context = {
        'dest': dest,
        'restaurant_types': restaurant_types,
        'amenity_types': amenity_types,
        'edit': edit,
    }
    return render(request, 'travel/map.html', context)
def plan_route(request, dest_id):
    dest = get_object_or_404(Destination, pk=dest_id)
    map = json.loads(dest.mapjson)
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
    print('----- node_ids = ', node_ids)
    # 调用路径规划算法
    if len(node_ids) == 2:
        planned_node_ids = route_sgl(map, node_ids[0], node_ids[1], mode)
    elif len(node_ids) > 2:
        planned_node_ids = route_mul(map, node_ids[1:], node_ids[0], mode)
    else:
        planned_node_ids = []
    # 由node_id获得经纬度序列 [[lat2,lon1], [lat2,lon2], ...]
    lat_lon_seq = [[map['nodes'][id]['lat'], map['nodes'][id]['lon']] for id in planned_node_ids]
    
    return JsonResponse({'latLonSeq': lat_lon_seq})
    
def search_amenity(request, dest_id):
    ''' 返回选中景点附近的设施 '''
    dest = get_object_or_404(Destination, pk=dest_id)
    map = json.loads(dest.mapjson)
    
    attr_id = int(request.GET.get('id'))
    amenity_type = request.GET.get('type', '')
    edit = request.GET.get('edit') == '1'

    # 在map找到对应景点
    selected_attraction = \
        map['nodes'][map['entrance']] if id == -1 \
        else map['attractions'][attr_id]
    
    amenities = map['amenities'] # 所有设施

    # 类别筛选
    if amenity_type != '':
        amenities = type_filter(amenities, lambda x: x['type'], amenity_type)
    # 计算距离，得到元组列表(distance, amenity)
    tuples = [(distance(
            x['lat'],
            x['lon'],
            selected_attraction['lat'],
            selected_attraction['lon']
            ), x) for x in amenities]
    # 排序
    tuples = attr_sort(tuples, lambda x: x[0], reverse=True)
    # 取距离 < AMENITY_SEARCH_RADIUS 的
    distances, amenities = zip(*tuples)
    r = bisect.bisect_right(distances, settings.AMENITY_SEARCH_RADIUS if not edit else 10000)

    return JsonResponse({'amenities': amenities[:r], 'distances': distances[:r]})

def search_restaurant(request, dest_id):
    ''' 返回选中景点附近的美食 '''
    dest = get_object_or_404(Destination, pk=dest_id)
    map = json.loads(dest.mapjson)
    
    attr_id = int(request.GET.get('id'))
    search_type = request.GET.get('search_type')
    search = request.GET.get('search', '')
    sort = request.GET.get('sort')
    filter = request.GET.get('filter')
    edit = request.GET.get('edit') == '1'
    arr_len = 0 if edit else 10

    # 在map找到对应景点
    selected_attraction = \
        map['nodes'][map['entrance']] if id == -1 \
        else map['attractions'][attr_id]
    
    restaurants = map['restaurants'] # 所有餐馆

    # 搜索框筛选
    if search != '':
        if search_type == '美食名称':
            restaurants = str_filter(restaurants, lambda x: ' '.join(x['foods']), search)
        elif search_type == '餐馆名称':
            restaurants = str_filter(restaurants, lambda x: x['name'], search)
    # print('----- str filter:', *restaurants, sep='\n')
    # 按菜系筛选
    if filter != '所有菜系':
        restaurants = type_filter(restaurants, lambda x: x['type'], filter)
    # print('----- type filter:', *restaurants, sep='\n')
    # 排序
    tuples = [(distance(
        x['lat'],
        x['lon'],
        selected_attraction['lat'],
        selected_attraction['lon']
        ), x) for x in restaurants]
    if sort == '热度最高':
        tuples = attr_sort(tuples, lambda t: t[1]['popularity'], l=arr_len)
    elif sort == '评分最高':
        tuples = attr_sort(tuples, lambda t: t[1]['rating'], l=arr_len)
    elif sort == '距离最近':
        tuples = attr_sort(tuples, lambda t: t[0], l=arr_len, reverse=True)
    distances, restaurants = zip(*tuples) if len(tuples) else [tuple(),tuple()]

    return JsonResponse({'restaurants': restaurants, 'distances': distances})


def update_coord(request, dest_id):
    dest = get_object_or_404(Destination, pk=dest_id)
    map = json.loads(dest.mapjson)
    # 从请求体中获取 JSON 数据
    data = json.loads(request.body)
    arr_name = data.get('arr_name')
    id = int(data.get('id'))
    lat = data.get('lat')
    lon = data.get('lon')

    target = map[arr_name][id]
    target['lat'] = round(lat, 6)
    target['lon'] = round(lon, 6)
    dest.mapjson = json.dumps(map, ensure_ascii=False, indent=4)
    print('before: ', target)
    dest.save()
    print('after: ', target)

    # 同步更新到文件
    if map['name'] == '北京动物园':
        map_id = 1
    with open(f'static/maps/{map_id}.json', 'w', encoding='utf-8') as f:
        json.dump(map, f, ensure_ascii=False, indent=4)

    return JsonResponse({'success': True})
