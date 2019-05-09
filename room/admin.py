from django.contrib import admin
from room.models import Room, Participant, Issue


class ParticipantInlineAdmin(admin.TabularInline):

    model = Participant
    readonly_fields = ('uid', 'created',)
    extra = 0


class IssueInlineAdmin(admin.TabularInline):

    model = Issue
    readonly_fields = ('uid', 'created',)
    extra = 0


class RoomAdmin(admin.ModelAdmin):

    exclude = ()
    list_display = ('uid', 'title', 'description', 'updated', 'created',)
    readonly_fields = ('uid', 'updated', 'created',)

    inlines = [ParticipantInlineAdmin, IssueInlineAdmin]


admin.site.register(Room, RoomAdmin)
