import jwt
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.base_model import BaseModel


class Room(BaseModel):
    """
        Data model for Room

    """

    title = models.CharField(verbose_name=_("Title"), max_length=128)

    description = models.TextField(verbose_name=_("Description"))

    current_issue = models.ForeignKey(
        'room.Issue', verbose_name=_('Current Issue'),
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='rooms'
    )

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
        ordering = ("-created",)

    def __str__(self):
        """returns title as Unicode “representation” of Room object."""
        return self.title

    @property
    def creator(self):
        return Participant.objects.filter(
            room=self, is_creator=True
        ).order_by("-created").first()


class Participant(BaseModel):
    """
        Data model for Participant

    """

    room = models.ForeignKey(Room, verbose_name=_('Room'),
                             on_delete=models.CASCADE,
                             related_name="participants")

    name = models.CharField(verbose_name=_("name"), max_length=128)

    is_creator = models.BooleanField(verbose_name=_("Is Creator"),
                                     default=False)

    class Meta:
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")
        ordering = ("-created",)
        unique_together = ['room', 'name']

    def __str__(self):
        """returns name as Unicode “representation” of Participant object."""
        return self.name

    @property
    def access_token(self):
        return jwt.encode(
            payload={"participant_uid": self.uid, "room_uid": self.room.uid},
            key=settings.JWT_SECRET_KEY
        )


class Issue(BaseModel):
    """
        Data model for Issue

    """

    room = models.ForeignKey(Room, verbose_name=_('Room'),
                             on_delete=models.CASCADE,
                             related_name="issues")

    number = models.CharField(verbose_name=_("Number"), max_length=32,
                              null=True, blank=True)

    title = models.TextField(verbose_name=_("Title"))

    vote_cards_status = models.CharField(
        verbose_name=_("Vote Cards Status"),
        max_length=32,
        choices=settings.ISSUE_VOTE_CARDS_STATUS_CHOICES,
        default=settings.HIDDEN
    )

    estimated_points = models.CharField(
        verbose_name=_("Estimated Points"),
        max_length=32,
        choices=settings.STORY_POINT_CHOICES,
        null=True, blank=True
    )

    class Meta:
        verbose_name = _("Issue")
        verbose_name_plural = _("Issues")
        ordering = ("-created",)

    def __str__(self):
        """returns title as Unicode “representation” of Issue object."""
        return self.title

    @property
    def is_current(self):
        return self.room.current_issue == self


class Vote(BaseModel):
    """
        Data model for Vote

    """

    issue = models.ForeignKey(Issue, verbose_name=_('Issue'),
                              on_delete=models.CASCADE, related_name='votes')

    participant = models.ForeignKey(Participant,
                                    verbose_name=_('Participant'),
                                    on_delete=models.CASCADE,
                                    related_name='votes')

    estimated_points = models.CharField(
        verbose_name=_("Estimated Points"),
        max_length=32,
        choices=settings.STORY_POINT_CHOICES,
        null=True, blank=True
    )

    class Meta:
        verbose_name = _("Vote")
        verbose_name_plural = _("Votes")
        ordering = ("-created",)

    def __str__(self):
        """returns id as Unicode “representation” of Vote object."""
        return self.uid
