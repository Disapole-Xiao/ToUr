from django.contrib import admin

from .models import User, Destination, Diary

admin.site.register([User, Destination, Diary])