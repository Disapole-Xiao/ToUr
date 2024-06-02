from django.contrib import admin

from .models import Diary, UserRating

class DiaryAdmin(admin.ModelAdmin):
    model = Diary
    list_display = ('title', 'location', 'author', 'rating', 'popularity', 'pub_time')
    list_filter = ('author',)  # 注意这里使用了元组格式
    search_fields = ('title', 'author', 'location')  # 注意这里使用了元组格式

class UserRatingAdmin(admin.ModelAdmin):
    model = UserRating
    list_display = ('author', 'diary', 'rating')
    list_filter = ('author', 'diary')  # 注意这里使用了元组格式
    search_fields = ('author', 'diary')
admin.site.register(Diary, DiaryAdmin)
admin.site.register(UserRating, UserRatingAdmin)