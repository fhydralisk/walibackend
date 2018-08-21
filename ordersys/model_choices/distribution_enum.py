from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


class _LTypeChoice(FieldChoice):
    MAX_LENGTH = 4
    CHOICE_DISPLAY = (
        (1, _("Forward Logistics"), "FORWARD"),
        (2, _("Backward Logistics"), "RETURN"),
    )


l_type_choice = _LTypeChoice()
