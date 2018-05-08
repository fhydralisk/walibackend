from django.forms import ModelForm
from usersys.models import UserValidatePhoto


class ValidatePhotoUploadForm(ModelForm):

    class Meta:
        model = UserValidatePhoto
        fields = ('v_photo',)
