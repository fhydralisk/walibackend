from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


class _SignStatusChoice(FieldChoice):
    MAX_LENGTH = 4
    CHOICE_DISPLAY = (
        (0, _("Not Signed"), "NOT_SIGNED"),
        (1, _("Accepted"), "ACCEPTED"),
        (2, _("Rejected"), "REJECTED"),
    )


class _SignMethodChoice(FieldChoice):
    MAX_LENGTH = 4
    CHOICE_DISPLAY = (
        (1, _("Accept"), "ACCEPT"),
        (2, _("Reject"), "REJECT"),
    )


sign_status_choice = _SignStatusChoice()
sign_method_choice = _SignMethodChoice()
