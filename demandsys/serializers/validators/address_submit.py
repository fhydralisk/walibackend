from rest_framework.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class AddressChoiceValidator(object):
    def __call__(self, attrs):

        abid = attrs.get('abid', None)
        aid = attrs.get('aid', None)
        street = attrs.get('street', None)  # type: str
        street = None if street is not None and len(street.strip()) == 0 else street

        if abid is None and (aid is None or street is None):
            raise ValidationError("Either abid or (aid, street) must be set", 400)
        return attrs
