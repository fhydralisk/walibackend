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


unit_choice = _UnitChoice()
t_demand_choice = _TDemandChoice()
freight_payer_choice = _FreightPayerChoice()
