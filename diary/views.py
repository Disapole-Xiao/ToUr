from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static

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

