from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static

from .models import Diary
def diary(request):
    diaries = Diary.objects.order_by('-pub_time') ## 修改成自己写的排序
    context = {
        'diaries': diaries,
    }
    return render(request, 'diary/index.html', context)

def detail(request, diary_id):
    diary = get_object_or_404(Diary, pk=diary_id)
    author_avatar_url = diary.author.avatar.url if \
        diary.author.avatar else \
        static("img/default_avatar.jpg")
    context = {
        'diary': diary,
        "author_avatar_url": author_avatar_url
    }
    return render(request, 'diary/detail.html', context)

