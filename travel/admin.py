from django.contrib import admin

# Register your models here.
from .models import Destination, Category

admin.site.register(Destination)
admin.site.register(Category)