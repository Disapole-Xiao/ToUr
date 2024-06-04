from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter

from .models import Diary, UserRating

class IsCompressedFilter(SimpleListFilter):
    title = _('Is Compressed')
    parameter_name = 'is_compressed'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(content_compressed__isnull=False)
        elif self.value() == 'no':
            return queryset.filter(content_compressed__isnull=True)
        return queryset
    

class DiaryAdmin(admin.ModelAdmin):
    model = Diary
    list_display = ('id', 'title', 'location', 'author', 'rating', 'popularity', 'pub_time', 'is_compressed')
    list_filter = ('author', IsCompressedFilter)  # 注意这里使用了元组格式
    search_fields = ('title', 'author', 'location')  # 注意这里使用了元组格式
    list_display_links = ('id', 'title')
    def get_search_results(self, request, queryset, search_term):
        # 重写搜索结果以支持自定义搜索字段
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(
                models.Q(title__icontains=search_term) |
                models.Q(author__icontains=search_term) |
                models.Q(location__icontains=search_term) |
                models.Q(is_compressed__icontains=search_term)
            )
        return queryset, use_distinct


class UserRatingAdmin(admin.ModelAdmin):
    model = UserRating
    list_display = ('id', 'author', 'diary', 'rating')
    list_filter = ('author', 'diary')  # 注意这里使用了元组格式
    search_fields = ('author', 'diary')
    list_display_links = ('id', 'author')

admin.site.register(Diary, DiaryAdmin)
admin.site.register(UserRating, UserRatingAdmin)