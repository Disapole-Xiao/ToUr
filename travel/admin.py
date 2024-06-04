from django.contrib import admin

from .models import *

class DestinationAdmin(admin.ModelAdmin):
    model = Destination
    list_display = ('id', 'name', 'type', 'province', 'city', 'popularity', 'rating', 'get_tags')
    list_filter = ('type', 'tags', 'province', )
    search_fields = ('name',)
    list_display_links = ('id', 'name')
    def get_tags(self, obj) -> str:
        return ", ".join([str(tag) for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'

admin.site.register(Destination, DestinationAdmin)
admin.site.register(Category)
admin.site.register(AmenityType)
admin.site.register(RestaurantType)