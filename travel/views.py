from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Destination, Category
from diary.models import Diary

import json
from src.map import Map
from src.routing import route_sgl, route_mul
from src.recommend import sort, name_filter, tag_filter, type_filter
# Create your views here.
def index(request):
    # 获取默认展示的游学地列表 ### 需要修改成综合排序
    dests = Destination.objects.all()
    # dests = sort(dest, '嗯嗯综合', conti=False, reverse=False, len=10) 从大到小排
    catagories = Category.objects.all()
    context = {
        'dests': dests,
        'catagories': catagories,
    }
    
    return render(request, 'travel/index.html', context)

def detail(request, dest_id):
    dest = get_object_or_404(Destination, pk=dest_id)
    related_diaries = Diary.objects.filter(location=dest).order_by('-rating')
    context = {
        'dest': dest,
        'related_diaries': related_diaries,
    }
    return render(request, 'travel/detail.html', context)
def map(request, dest_id):
    dest = get_object_or_404(Destination, pk=dest_id)
    cuisine_types = {"川湘菜", "西餐", "新疆菜", "日韩菜"} ##
    amenity_types = {"厕所", "快递站", "超市"}
    context = {
        'dest': dest,
        'cuisine_types': cuisine_types,
        'amenity_types': amenity_types,
    }
    return render(request, 'travel/map.html', context)

def plan_route(request, dest_id):
    print('!!!!!')
    dest = get_object_or_404(Destination, pk=dest_id)
    print('!!!!!!!!!', 'dest')
    map = json.loads(dest.mapjson)
    print('!!!!!!!!',' map')
    if request.method == 'POST':
        # 从请求体中获取 JSON 数据
        data = json.loads(request.body)
        print(request.body)
        selected_attractions = data.get('selected_attractions')
        print(selected_attractions)
        selected_attractions = [int(attr_id) if attr_id != None else None for attr_id in selected_attractions]
        print(selected_attractions)
        mode = data.get('mode')
        
        # 这里可以对景点数据进行处理，比如路径规划等
        node_ids = []
        # 将 attractions 映射到 node
        if selected_attractions[0] == None:
            node_ids.append(map['entrance'])
            print('append', node_ids)
        node_ids += [map['attractions'][attr_id]['entr_point'][0] for attr_id in selected_attractions if attr_id != None]
        print('!!!!!!!!',node_ids)
        if len(node_ids) == 2:
            planned_node_ids = route_sgl(map, node_ids[0], node_ids[1], mode)
        elif len(node_ids) > 2:
            planned_node_ids = route_mul(map, node_ids[1:], node_ids[0], mode)
        # 由node_id获得经纬度序列 [[lat2,lon1],[lat2,lon2]]
        lat_lon_seq = [[map['nodes'][id]['lat'], map['nodes'][id]['lon']] for id in planned_node_ids]
        # 返回 JSON 响应，包含路径信息等
        return JsonResponse({'latLonSeq': lat_lon_seq})