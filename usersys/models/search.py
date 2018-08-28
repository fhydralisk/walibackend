from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from usersys.models import UserBase


class SearchHistory(models.Model):
    uid = models.ForeignKey(
        UserBase,
        on_delete=models.CASCADE,
        related_name="search_history",
        verbose_name=_("user"),
    )
    keyword = models.CharField(max_length=60)
