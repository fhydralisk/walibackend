from django.forms import ModelForm
from invitesys.models import InviteContractTemplate


class InviteContractTemplateUploadForm(ModelForm):

    class Meta:
        model = InviteContractTemplate
        fields = ('contract_template',)
