from django import forms
from django.forms import ModelForm
from .models import Certificate
import uuid
from users.models import CustomUser

# from django.template.defaultfilters import

class PreCertificate(ModelForm):

    class Meta:
        model = Certificate
        fields = [  'internal_num','is_published',]

class EditProfileForm(ModelForm):

    company_name = forms.CharField(empty_value="Company name", required=True)

    class Meta:
        model = CustomUser
        fields = [ 'company_name',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_name'].widget.attrs.update({'class': 'form-control-plaintext bg-success rounded h6'})
