from django.contrib import admin
from room.models import Room


class RoomAdmin(admin.ModelAdmin):

    exclude = ()
    list_display = ('uid', 'title', 'description', 'updated', 'created',)
    readonly_fields = ('uid', 'updated', 'created',)


admin.site.register(Room, RoomAdmin)
