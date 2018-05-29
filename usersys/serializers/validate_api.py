from collections import OrderedDict, Mapping

from rest_framework import serializers
from usersys.models.user_enum import t_photo_choice
from usersys.models import UserValidate, UserValidateArea


class ValidationPhotoSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    t_photo = serializers.ChoiceField(choices=t_photo_choice.get_choices())


class ValidationInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserValidate
        fields = '__all__'
        read_only_fields = ('id', 'uid', 'validate_status')


class ValidationInfoSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserValidate
        exclude = ('id', 'uid', 'validate_status')


class ValidationAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserValidateArea
        exclude = ('vid', 'id')

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                # Be Careful, if the following line is not added,
                # it may throw an error when deserializing a partial
                # constructed object.
                if isinstance(instance, Mapping):
                    if field.field_name not in instance:
                        continue

                # End

                attribute = field.get_attribute(instance)
            except serializers.SkipField:
                continue

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, serializers.PKOnlyObject) else attribute
            if check_for_none is None:
                # ret[field.field_name] = None
                pass
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret


class ValidationSubmitSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    validate_request = serializers.IntegerField(required=False)
    validate_obj = ValidationInfoSubmitSerializer(required=False)
    # TODO: Add area validators!
    validate_areas = ValidationAreaSerializer(many=True, required=False, partial=True)


class ValidationInfoDisplaySeralizer(serializers.Serializer):
    validate_obj = ValidationInfoSerializer(read_only=True)
    validate_areas = ValidationAreaSerializer(many=True, read_only=True)
    validate_photos_uploaded = serializers.SlugRelatedField(slug_field='t_photo', many=True, read_only=True)


class ValidationInfoInvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserValidate
        fields = ('company', 'phonenum', 'address', 'texno', 'obank', 'bankcard')
