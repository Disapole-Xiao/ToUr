from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.http import JsonResponse

from travel.models import Destination
from account.models import CustomUser
from .models import Diary
from src.recommend import attr_sort, str_filter, tag_filter, type_filter

def index(request):
    diaries = list(Diary.objects.all())
    search_type = request.GET.get('search_type', '日记名称')
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '时间最新')
    print(request.GET)
    # 搜索框不为空，按search_type筛选
    if search != '':
        if search_type == '日记名称':
            diaries = str_filter(diaries, 'title', search)
        elif search_type == '游学地名称':
            pass
        elif search_type == '全文搜索':
            diaries = str_filter(diaries, 'content', search)
    print('search:', *diaries, sep='\n')
    # 排序
    attr = 'pub_time'
    if sort == '时间最新':
        attr = 'pub_time'
    elif sort == '热度最高':
        attr = 'popularity'
    elif sort == '评分最高':
        attr = 'rating' 
    diaries = attr_sort(diaries, attr, len = 9)
    print('sort:', *diaries, sep='\n')

    context = {
        'diaries': diaries,
        'search_type': search_type,
        'search': search,
        'sort': sort,
    }
    return render(request, 'diary/index.html', context)

def detail(request, diary_id):
    diary = get_object_or_404(Diary, pk=diary_id)
    default_avatar_url = static("img/default_avatar.jpg")
    context = {
        'diary': diary,
        'default_avatar_url': default_avatar_url,
    }
    return render(request, 'diary/detail.html', context)

@require_http_methods(["POST"])
def add_diary(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        location_name = request.POST.get('location')
        location = get_object_or_404(Destination, name=location_name)
        author = get_object_or_404(CustomUser, username='小明')
        new_diary = Diary(author=author, title=title, content=content, location=location)
        # new_diary = Diary(author=request.user, title=title, content=content, location=location)
        new_diary.save()
        return redirect('/diary/')  # Redirect to a new URL after saving

# 在日记添加表单中处理搜索游学地
def search_location(request):
    query = request.GET.get('query', '')
    if query:
        destinations = Destination.objects.filter(name__icontains=query)
        results = [{'id': dest.id, 'name': dest.name} for dest in destinations]
    else:
        results = []
    return JsonResponse(results, safe=False)