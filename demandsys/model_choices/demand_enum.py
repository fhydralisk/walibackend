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


class _FreightPayerChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _("Seller pay freight."), "FREIGHT_BUYER"),
        (2, _("Buyer pay freight"), "FREIGHT_SELLER"),
    )


unit_choice = _UnitChoice()
t_demand_choice = _TDemandChoice()
freight_payer_choice = _FreightPayerChoice()
