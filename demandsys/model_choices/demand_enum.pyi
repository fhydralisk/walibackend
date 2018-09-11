from base.util.field_choice import FieldChoice


class _UnitChoice(FieldChoice):
    T = None
    KG = None


class _TDemandChoice(FieldChoice):
    BUY = None
    SELL = None


class _FreightPayerChoice(FieldChoice):
    FREIGHT_BUYER = None
    FREIGHT_SELLER = None


class _MatchOrderChoice(FieldChoice):
    SCORE = None
    PRICE = None
    QUANTITY = None


class _IntervalChoice(FieldChoice):
    JUST_NOW = None
    AN_HOUR_AGO = None
    SIX_HOURS_AGO = None
    A_DAY_AGO = None
    TWO_DAYS_AGO = None
    TEN_DAYS_AGO = None
    A_MONTH_AGO = None


class _ProductT1idChoice(FieldChoice):
    PET = None
    IRON = None
    PAPER = None


unit_choice = _UnitChoice()
t_demand_choice = _TDemandChoice()
freight_payer_choice = _FreightPayerChoice()
match_order_choice = _MatchOrderChoice()
interval_choice = _IntervalChoice()
product_t1id_choice = _ProductT1idChoice()

