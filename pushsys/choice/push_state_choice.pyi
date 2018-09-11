from base.util.field_choice import FieldChoice

class _PushStateChoice(FieldChoice):
    ORDERINFO_O_STATUS = None
    INVITEINFO_I_STATUS = None
    SIMPLIFIED_INVITEINFO_I_STATUS = None


push_state_choice = _PushStateChoice()
