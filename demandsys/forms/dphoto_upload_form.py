from django.forms import ModelForm
from usersys.models import UserValidatePhoto


class UploadPhotoForm(ModelForm):

    class Meta:
        model = UserValidatePhoto
        fields = ('demand_photo',)
