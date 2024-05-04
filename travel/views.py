from django.shortcuts import get_object_or_404, render
from .models import Destination
from src.map import Map
# Create your views here.
def index(request):
    # 获取默认展示的游学地列表 ### 需要修改成综合排序
    dests = Destination.objects.all()
    # dests = sort(dest, '嗯嗯综合', conti=False, reverse=False, len=10) 从大到小排
    context = {
        'dests': dests,
    }
    
    return render(request, 'travel/index.html', context)

def detail(request, dest_id):
    dest = get_object_or_404(Destination, pk=dest_id)
    context = {
        'dest': dest
    }
    return render(request, 'travel/detail.html', context)
def map(request, dest_id):
    dest = get_object_or_404(Destination, pk=dest_id)
    map = Map(dest.mapjson) # 实例化一个Map对象
    context = {
        'map': map,
        'dest': dest
    }
    return render(request, 'travel/map.html', context)
