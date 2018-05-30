from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


class _UnitChoice(FieldChoice):
    MAX_LENGTH = 4
    CHOICE_DISPLAY = (
        (1, _("T"), "T"),
        (2, _("KG"), "KG"),
    )


class _TDemandChoice(FieldChoice):
    MAX_LENGTH = 4
    CHOICE_DISPLAY = (
        (0, _("Buy"), "BUY"),
        (1, _("Sell"), "SELL"),
    )


unit_choice = _UnitChoice()
t_demand_choice = _TDemandChoice()
