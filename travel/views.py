import json, bisect, math
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

from .models import Destination, Category, AmenityType, RestaurantType
from diary.models import Diary
from .funcs import distance, comprehensive_tuple, make_route_key
from src.routing import route_sgl, route_mul
from src.recommend import attr_sort, str_filter, tag_filter, type_filter

@login_required
def index(request):
    context = {
        'tags': [tag.name for tag in Category.objects.all()]
    }
    return render(request, 'travel/index.html', context)

@login_required
def load_dests(request):
    ''' 加载（更多）游学地 '''
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '兴趣推荐')
    category = request.GET.get('category', '所有类别')
    page = int(request.GET.get('page')) # 当前请求的页
    
    load_more = page > 1 # 判断是否是继续加载的请求
    

    # 如果继续加载，不需要重新过滤，从缓存读取
    if load_more:
        dests = cache.get('filtered_dests')
    # 否则重新筛选
    else:
        dests = list(Destination.objects.all())
        # 搜索框不为空，按名字筛选
        if search != '':
            dests = str_filter(dests, lambda x: x.name, search)
        # print('----- str filter:', *dests, sep='\n')
        # 类别筛选
        if category != '所有类别':
            dests = tag_filter(dests, lambda x: x.tags.all(), Category.objects.get(name=category))
        # print('----- tag fliter:', *dests, sep='\n')
        cache.set('filtered_dests', dests)  # 缓存过滤后的结果

    PAGE_LEN = 8
    TOTAL_PAGE_NUM = math.ceil(len(dests) / PAGE_LEN) # 总页数
    print('----- total dest num:', len(dests))
    print('----- total page num:', TOTAL_PAGE_NUM)
    print('----- current page:', page)

    # 排序
    if sort == '兴趣推荐':
        dests = attr_sort(dests, lambda x: comprehensive_tuple(x, request.user), 'dest', l=PAGE_LEN, conti=load_more)
    elif sort == '热度最高':
        dests = attr_sort(dests, lambda x: x.popularity, 'dest', l=PAGE_LEN, conti=load_more)
    elif sort == '评分最高':
        dests = attr_sort(dests, lambda x: x.rating, 'dest', l=PAGE_LEN, conti=load_more)
    
    dest_list = render_to_string('travel/dest_list.html', {'dests': dests})
    has_next = page < TOTAL_PAGE_NUM # 判断是否还有下一页
    return JsonResponse({'destListHtml': dest_list, 'hasNext': has_next})

@login_required
def detail(request, dest_id):
    ''' 游学地详细界面 '''
    dest = get_object_or_404(Destination, pk=dest_id)
    related_diaries = Diary.objects.filter(location=dest).order_by('-rating')
    context = {
        'dest': dest,
        'related_diaries': related_diaries,
    }
    return render(request, 'travel/detail.html', context)

@login_required
def map(request, dest_id, edit=False):
    dest = get_object_or_404(Destination, pk=dest_id)

    restaurant_types = [x.name for x in RestaurantType.objects.all()]
    amenity_types = [x.name for x in AmenityType.objects.all()]
    map_json = dest.get_map()
    context = {
        'dest': dest,
        'restaurant_types': restaurant_types,
        'amenity_types': amenity_types,
        'edit': edit,
        'map_json': map_json,
        'restaurant': RestaurantType.objects.all()[0]
    }
    return render(request, 'travel/map.html', context)

@login_required
def plan_route(request, dest_id):
    # 从请求体中获取 JSON 数据
    data = json.loads(request.body)
    selected_attractions = data.get('selected_attractions')
    selected_attractions = [int(attr_id) for attr_id in selected_attractions]
    mode = data.get('mode')
    allow_ride = data.get('allow_ride')
    print('----- selected_attractions = ', selected_attractions)

    key = make_route_key(selected_attractions, mode, allow_ride)
    # 缓存
    map_id, routes = cache.get('routing', (None,None))
    if map_id and map_id == dest_id:
        try:
            print('----- routes: ', routes) 
            return JsonResponse(routes[key])
        except: pass
    else:
        routes = {}
    
    dest = get_object_or_404(Destination, pk=dest_id)
    map = json.loads(dest.get_map())

    # 将 attractions 映射到 node，入口特殊处理
    node_ids = [map['entrance'] if attr_id == -1 
                else map['attractions'][attr_id]['entr_point'][0] 
                for attr_id in selected_attractions]
    print('----- node_ids = ', node_ids)

    node_attr_dict = dict(zip(node_ids, selected_attractions)) # 一一对应

    # 调用路径规划算法 单目标 多目标
    planned_node_ids = []
    cost = None
    entr_point_order = []
    if allow_ride:
        vehicle = 'bicycle' if dest.type == 'u' else 'motorbike'
    else:
        vehicle = None
    if len(node_ids) == 2:
        planned_node_ids, cost  = route_sgl(map, node_ids[0], node_ids[1], mode=mode, vehicle=vehicle)
    elif len(node_ids) > 2:
        planned_node_ids, cost, entr_point_order = route_mul(map, node_ids[1:], node_ids[0], mode=mode, vehicle=vehicle)

    # 由node_id获得经纬度序列 [[lat2,lon1], [lat2,lon2], ...]
    lat_lon_seq = [[map['nodes'][id]['lat'], map['nodes'][id]['lon']] for id in planned_node_ids]
    # 入口点顺序转换为景点游览顺序
    attr_order = [node_attr_dict[node] for node in entr_point_order]
    print('----- attr_order = ', attr_order)

    routes[key] = {
        'latLonSeq': lat_lon_seq,
        'cost': cost,
        'attractionOrder': attr_order
    }
    cache.set('routing', (dest_id, routes))
    return JsonResponse(routes[key])
    
@login_required
def search_amenity(request, dest_id):
    ''' 返回选中景点附近的设施 '''
    dest = get_object_or_404(Destination, pk=dest_id)
    map = json.loads(dest.get_map())
    
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
    tuples = attr_sort(tuples, lambda x: x[0], 'amenity', ascend=True)
    # 取距离 < AMENITY_SEARCH_RADIUS 的
    distances, amenities = zip(*tuples)
    r = bisect.bisect_right(distances, settings.AMENITY_SEARCH_RADIUS if not edit else 10000)

    return JsonResponse({'amenities': amenities[:r], 'distances': distances[:r]})

@login_required
def search_restaurant(request, dest_id):
    ''' 返回选中景点附近的美食 '''
    dest = get_object_or_404(Destination, pk=dest_id)
    map = json.loads(dest.get_map())
    
    attr_id = int(request.GET.get('id'))
    search_type = request.GET.get('search_type')
    search = request.GET.get('search', '')
    sort = request.GET.get('sort')
    filter = request.GET.get('filter')
    edit = request.GET.get('edit') == '1'
    arr_len = None if edit else 10

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
        tuples = attr_sort(tuples, lambda t: t[1]['popularity'], 'restaurant', l=arr_len)
    elif sort == '评分最高':
        tuples = attr_sort(tuples, lambda t: t[1]['rating'], 'restaurant', l=arr_len)
    elif sort == '距离最近':
        tuples = attr_sort(tuples, lambda t: t[0], 'restaurant', l=arr_len, ascend=True)
    distances, restaurants = zip(*tuples) if len(tuples) else [tuple(),tuple()]

    return JsonResponse({'restaurants': restaurants, 'distances': distances})

@login_required
def update_coord(request, dest_id):
    dest = get_object_or_404(Destination, pk=dest_id)
    map = json.loads(dest.get_map())
    # 从请求体中获取 JSON 数据
    data = json.loads(request.body)
    arr_name = data.get('arr_name')
    id = int(data.get('id'))
    lat = data.get('lat')
    lon = data.get('lon')

    target = map[arr_name][id]
    target['lat'] = round(lat, 6)
    target['lon'] = round(lon, 6)
    dest.set_map(json.dumps(map, ensure_ascii=False, indent=4))
    print('before: ', target)
    dest.save() # save操作会自动压缩
    print('after: ', target)

    # 同步更新到文件
    if map['name'] == '北京动物园':
        map_id = 1 
    elif map['name'] == '北京大学':
        map_id = 2
    elif map['name'] == '清华大学':
        map_id = 3
    elif map['name'] == '故宫博物院':
        map_id = 4
    with open(f'static/maps/{map_id}.json', 'w', encoding='utf-8') as f:
        json.dump(map, f, ensure_ascii=False, indent=4)
    cache.delete('map_json')

    return JsonResponse({'success': True})
