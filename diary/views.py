from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.http import JsonResponse

from travel.models import Destination
from account.models import User
from .models import Diary
def diary(request):
    ## 修改成自己写的排序
    diaries = Diary.objects.order_by('-pub_time') 
    # diaries = sort(diaries, '嗯嗯综合', conti=False, reverse=False, len=10) 从大到小排
    context = {
        'diaries': diaries,
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
        author = get_object_or_404(User, username='小明')
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