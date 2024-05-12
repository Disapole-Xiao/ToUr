from django.shortcuts import get_object_or_404, render
from .models import Destination, Category
from diary.models import Diary
from src.map import Map
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
    cuisines = {"川湘菜", "西餐", "新疆菜", "日韩菜"} ##
    context = {
        'dest': dest,
        'cuisines': cuisines,
    }
    return render(request, 'travel/map.html', context)