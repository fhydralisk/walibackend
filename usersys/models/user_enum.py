from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


class _RoleChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _("Buyer"), "BUYER"),
        (2, _("Seller"), "SELLER"),
    )


class _TUserChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _("Enterprise User"), "ENTERPRISE_USER"),
        (2, _("Individual User"), "INDIVIDUAL_USER")
    )


class _ValidateStatusChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, _("Not committed"), "NOT_COMMITTED"),
        (1, _("Committed, not proceeded"), "NOT_PROCEEDED"),
        (2, _("Proceeded and accepted"), "ACCEPTED"),
        (4, _("Proceeded and rejected"), "REJECTED"),
    )


class _TPhotoChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (1, _("Business license"), "LICENSE"),
        (2, _("Top side of ID card"), "ID_TOP"),
        (3, _("Bottom side of ID card"), "ID_BOTTOM"),
    )


role_choice = _RoleChoice()
t_user_choice = _TUserChoice()
validate_status_choice = _ValidateStatusChoice()
t_photo_choice = _TPhotoChoice()
