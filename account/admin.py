# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'username', 'is_staff', 'get_interests')
    list_filter = ('is_staff',)  # 注意这里使用了元组格式
    search_fields = ('username',)  # 注意这里使用了元组格式
    list_display_links = ('id', 'username')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('avatar', 'interests', 'email')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    def get_interests(self, obj):
        return ", ".join([str(interest) for interest in obj.interests.all()])
    get_interests.short_description = 'Interests'

admin.site.register(CustomUser, CustomUserAdmin)
