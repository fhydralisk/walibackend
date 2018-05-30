from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError

from usersys.models import UserValidate
from usersys.model_choices.user_enum import validate_status_choice, role_choice, t_user_choice, t_photo_choice


@deconstructible
class UserValidateStatusValidator(object):
    """
    Validate the validate_status field for UserValidate Model
    """

    fields_to_validate = {
        role_choice.BUYER: {
            t_user_choice.ENTERPRISE_USER: ('contact', 'company', 'bankcard', 'obank', 'phonenum', 'texno', 'address')
        },
        role_choice.SELLER: {
            t_user_choice.ENTERPRISE_USER: ('contact', 'company', 'bankcard', 'obank', 'phonenum'),
            t_user_choice.INDIVIDUAL_USER: ('contact', 'bankcard', 'obank', 'idcard_number')
        }
    }

    def __init__(self, is_user=True):
        self.queryset = UserValidate.objects
        self.serializer_field = None
        self.is_user = is_user

    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the underlying model field name. This may not be the
        # same as the serializer field name if `source=<>` is set.
        self.field_name = "validate_status"
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer_field.parent, 'instance', None)
        self.updated_data = getattr(serializer_field.parent, 'initial_data', None)

    def ensure_user_vstatus(self, value):

        # Validate status
        if self.is_user and\
                value not in (validate_status_choice.NOT_COMMITTED, validate_status_choice.NOT_PROCEEDED):
            return False
        else:
            return True

    def ensure_fields(self, value):
        # Ensure each filed is filled
        if value != validate_status_choice.NOT_COMMITTED:
            if self.instance.t_user is None:
                return False
            try:
                fields_check = self.fields_to_validate[self.instance.uid.role][self.instance.t_user]
            except KeyError:
                raise ValidationError("user role, t_user is invalid", 403)

            for f in fields_check:
                if f in self.updated_data:
                    # Check user submitted data first
                    if self.updated_data[f] is None:
                        return False
                else:
                    # Check existing data next
                    if getattr(self.instance, f) is None:
                        return False

        return True

    def ensure_photos(self, value):
        # Ensure photos are uploaded
        if value != validate_status_choice.NOT_COMMITTED:
            photoobjs = self.instance.validate_photo.filter(inuse=True)
            if self.instance.t_user == t_user_choice.ENTERPRISE_USER:
                photoobjs = photoobjs.filter(t_photo=t_photo_choice.LICENSE)
                if not photoobjs.exists():
                    return False

            if self.instance.t_user == t_user_choice.INDIVIDUAL_USER:
                photo_id_top = photoobjs.filter(t_photo=t_photo_choice.ID_TOP)
                photo_id_bot = photoobjs.filter(t_photo=t_photo_choice.ID_BOTTOM)
                if not (photo_id_top.exists() and photo_id_bot.exists()):
                    return False
        return True

    def ensure_areas(self, value):
        # Ensure areas are submitted
        # FIXME: Check areas are in use.
        if value != validate_status_choice.NOT_COMMITTED:
            area_objs = self.instance.validate_area.filter(vid=self.instance)
            if not area_objs.exists():
                return False

        return True

    def validate_proc(self, func, value, message, code):
        if not func(value):
            raise ValidationError(message, code)

    def __call__(self, value):

        assert(value is not None)

        if self.updated_data is None:
            return

        if self.instance is None:
            return

        if value == validate_status_choice.NOT_COMMITTED:
            return

        if not self.is_user:
            # Admin always can modify this?
            return

        self.validate_proc(self.ensure_user_vstatus, value, "User do not have permission to change it to this value.", 401)
        self.validate_proc(self.ensure_fields, value, "Some of fields not filled", code=403)
        self.validate_proc(self.ensure_photos, value, "Photo fields must be appended before submit", code=403)
        self.validate_proc(self.ensure_areas, value, "Area fields must be appended before submit", code=403)


@deconstructible
class UserValidateTUserValidator(object):
    def __init__(self, is_user=True):
        self.queryset = UserValidate.objects
        self.serializer_field = None
        self.is_user = is_user

    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the underlying model field name. This may not be the
        # same as the serializer field name if `source=<>` is set.
        self.field_name = "validate_status"
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer_field.parent, 'instance', None)

    def ensure_role_match_tuser(self, value):
        # Validate if t_user matches role
        role = self.instance.uid.role
        if role == role_choice.BUYER:
            if value == t_user_choice.INDIVIDUAL_USER:
                return False

        if role == role_choice.SELLER:
            pass

        return True

    def __call__(self, value):
        if not self.ensure_role_match_tuser(value):
            raise ValidationError("Role do not match user type", code=400)
