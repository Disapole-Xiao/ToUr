from django.contrib import admin

# Register your models here.
from .models import CustomUser, Interest

admin.site.register(CustomUser)
admin.site.register(Interest)
