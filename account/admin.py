from django.contrib import admin

# Register your models here.
from .models import User, Interest

admin.site.register(User)
admin.site.register(Interest)