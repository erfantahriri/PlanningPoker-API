from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.helpers import generate_short_uuid


class BaseModel(models.Model):
    """
        Base Model for add uid, updated, created fields to all PlanningPoker
            models

    """

    class Meta:
        abstract = True

    uid = models.CharField(verbose_name=_("UID"), max_length=50,
                           default=generate_short_uuid, unique=True)

    updated = models.DateTimeField(verbose_name=_("Updated At"),
                                   null=True, auto_now=True)

    created = models.DateTimeField(verbose_name=_("Created At"),
                                   null=True, auto_now_add=True)
