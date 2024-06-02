import json, math
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.core.cache import cache

from travel.models import Destination
from .models import Diary, UserRating
from src.recommend import attr_sort, str_filter, tag_filter, type_filter
from travel.funcs import comprehensive_tuple

User = get_user_model

@login_required
def index(request):
    context = {
    }
    return render(request, 'diary/index.html', context)

@login_required
def load_diaries(request):
    ''' 加载（更多）日记 '''
    search_type = request.GET.get('search_type', '日记名称')
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '时间最新')
    page = int(request.GET.get('page', 1))

    load_more = page > 1

     # 如果继续加载，不需要重新过滤，从缓存读取
    if load_more:
        diaries = cache.get('filtered_diaries')
    # 否则重新筛选    
    else:
        diaries = list(Diary.objects.all())
        # 搜索框不为空，按search_type筛选
        if search != '':
            if search_type == '日记名称':
                diaries = str_filter(diaries, lambda x: x.title, search)
            elif search_type == '游学地名称':
                diaries = str_filter(diaries, lambda x: x.location.name, search)
            elif search_type == '全文搜索':
                diaries = str_filter(diaries, lambda x: x.content, search)
        # print('----- search:', *diaries, sep='\n')
        cache.set('filtered_diaries', diaries)  # 缓存过滤后的结果


    PAGE_LEN = 9
    TOTAL_PAGE_NUM = math.ceil(len(diaries) / PAGE_LEN) # 总页数
    print('----- total diary num:', len(diaries))
    print('----- total page num:', TOTAL_PAGE_NUM)
    print('----- current page:', page)
    
     # 排序
    if sort == '综合排序':
        diaries = attr_sort(diaries, lambda x: comprehensive_tuple(x.location, request.user), 'diary', ascend=False, l = PAGE_LEN)
    elif sort == '时间最新':
        diaries = attr_sort(diaries, lambda x: x.pub_time, 'diary', l=PAGE_LEN)
    elif sort == '热度最高':
        diaries = attr_sort(diaries, lambda x: x.popularity, 'diary', l=PAGE_LEN)
    elif sort == '评分最高':
        diaries = attr_sort(diaries, lambda x: x.rating, 'diary', l=PAGE_LEN)
    # print('----- sort:', *diaries, sep='\n')
    print(diaries)
    diary_list = render_to_string('diary/diary_list.html', {'diaries': diaries})
    has_next = page < TOTAL_PAGE_NUM # 判断是否还有下一页
    print(diary_list, has_next)
    return JsonResponse({'diaryListHtml': diary_list, 'hasNext': has_next})


@login_required
def detail(request, diary_id):
    diary = get_object_or_404(Diary, pk=diary_id)
    diary.popularity = diary.popularity + 1
    diary.save()
    try:
        user_rating = UserRating.objects.get(author=request.user, diary=diary).rating
    except UserRating.DoesNotExist:
        user_rating = 0
    context = {
        'diary': diary,
        'user_rating': user_rating
    }
    return render(request, 'diary/detail.html', context)

@login_required
@require_http_methods(["POST"])
def add_diary(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        location_name = request.POST.get('location')
        location = get_object_or_404(Destination, name=location_name)
        author = request.user
        new_diary = Diary(author=author, title=title, content=content, location=location)
        new_diary.save()
        return redirect('/diary/')  # Redirect to a new URL after saving

@login_required
@require_http_methods(["GET"])
def search_location(request):
    ''' 在日记添加表单中处理搜索游学地 '''
    query = request.GET.get('query', '')
    if query:
        destinations = Destination.objects.filter(name__icontains=query)
        results = [{'id': dest.id, 'name': dest.name} for dest in destinations]
    else:
        results = []
    return JsonResponse(results, safe=False)

@login_required
@require_http_methods(["POST"])
def rate(request, diary_id):
    # 解析 JSON 数据
        data = json.loads(request.body)
        rating = data.get('rating')
        rating = int(rating)  # 确保评分是正确的数据类型
        print('rating', rating)

        diary = get_object_or_404(Diary, pk=diary_id)
        UserRating.objects.update_or_create(
            author=request.user, 
            diary=diary, 
            defaults={'rating': rating}
        )

        # 重新计算平均评分
        diary.rating = UserRating.objects.filter(diary=diary).aggregate(avg_rating=Avg('rating'))['avg_rating']
        print('diary.rating', diary.rating)
        diary.save()
        return JsonResponse({'success': True})