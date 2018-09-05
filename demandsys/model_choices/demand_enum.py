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


class _MatchOrderChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _(""), "SCORE"),
        (2, _(""), "PRICE"),
        (3, _(""), "QUANTITY"),
    )


class _IntervalChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _(""), "JUST_NOW"),
        (2, _(""), "AN_HOUR_AGO"),
        (3, _(""), "SIX_HOURS_AGO"),
        (4, _(""), "A_DAY_AGO"),
        (5, _(""), "TWO_DAYS_AGO"),
        (6, _(""), "TEN_DAYS_AGO"),
        (7, _(""), "A_MONTH_AGO"),
    )


unit_choice = _UnitChoice()
t_demand_choice = _TDemandChoice()
freight_payer_choice = _FreightPayerChoice()
match_order_choice = _MatchOrderChoice()
interval_choice = _IntervalChoice()
