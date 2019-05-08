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
