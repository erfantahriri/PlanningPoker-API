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

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
        ordering = ("-created",)

    def __str__(self):
        """returns id as Unicode “representation” of Room object."""
        return self.uid


class Participant(BaseModel):
    """
        Data model for Participant

    """

    room = models.ForeignKey(Room, verbose_name=_('Room'),
                             on_delete=models.PROTECT)

    name = models.CharField(verbose_name=_("name"), max_length=128)

    class Meta:
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")
        ordering = ("-created",)
        unique_together = ['room', 'name']

    def __str__(self):
        """returns id as Unicode “representation” of Participant object."""
        return self.uid

    @property
    def access_token(self):
        return jwt.encode(
            payload={"participant_uid": self.uid, "room_uid": self.room.uid},
            key=settings.JWT_SECRET_KEY
        )
