from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from demandsys.models import ProductTypeL3


class QualityQuerySerializer(serializers.Serializer):
    pid = serializers.PrimaryKeyRelatedField(
        default=None, allow_null=True, queryset=ProductTypeL3.objects.filter(in_use=True)
    )
    id = serializers.IntegerField(
        default=None, allow_null=True,
        min_value=1,
        max_value=5,
    )

    def validate(self, attrs):
        p = attrs.get("pid", None)
        i = attrs.get("id", None)
        if not (p is None and i is not None or i is None and p is not None):
            raise ValidationError("Only one of pid, id must be filled.")

        return attrs
