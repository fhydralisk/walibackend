from django.forms import ModelForm
from demandsys.models import ProductDemandPhoto


class UploadPhotoForm(ModelForm):

    class Meta:
        model = ProductDemandPhoto
        fields = ('demand_photo',)

