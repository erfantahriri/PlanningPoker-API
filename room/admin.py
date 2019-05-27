from django.contrib import admin
from room.models import Room, Participant, Issue, Vote


class ParticipantInlineAdmin(admin.TabularInline):

    model = Participant
    readonly_fields = ('uid', 'created',)
    extra = 0


class VotesInlineAdmin(admin.TabularInline):

    model = Vote
    readonly_fields = ('uid', 'created',)
    extra = 0


class IssueInlineAdmin(admin.TabularInline):

    model = Issue
    readonly_fields = ('uid', 'created',)
    extra = 0


class RoomAdmin(admin.ModelAdmin):

    exclude = ()
    list_display = ('uid', 'title', 'description', 'issues_count',
                    'participants_count', 'updated', 'created',)
    readonly_fields = ('uid', 'updated', 'created',)

    inlines = [ParticipantInlineAdmin, IssueInlineAdmin]

    @staticmethod
    def issues_count(obj):
        """returns number of Issues for a Room"""
        return obj.issues.count()

    @staticmethod
    def participants_count(obj):
        """returns number of Participants for a Room"""
        return obj.participants.count()


class ParticipantAdmin(admin.ModelAdmin):

    exclude = ()
    list_display = ('uid', 'room', 'name', 'votes_count', 'is_creator',
                    'updated', 'created',)
    readonly_fields = ('uid', 'updated', 'created',)

    @staticmethod
    def votes_count(obj):
        """returns number of Votes for a Participant"""
        return obj.votes.count()


class IssueAdmin(admin.ModelAdmin):

    exclude = ()
    list_display = ('uid', 'room', 'number', 'title', 'estimated_points',
                    'vote_cards_status', 'votes_count', 'updated', 'created',)
    readonly_fields = ('uid', 'updated', 'created',)

    @staticmethod
    def votes_count(obj):
        """returns number of Votes for an Issue"""
        return obj.votes.count()

    inlines = [VotesInlineAdmin]


admin.site.register(Room, RoomAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Issue, IssueAdmin)
