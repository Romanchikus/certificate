from django import forms
from django.forms import ModelForm
from .models import Certificate
import uuid
from users.models import CustomUser

# from django.template.defaultfilters import

class PreCertificate(ModelForm):

    readonly_fields=('public_num',)
    class Meta:
        model = Certificate
        fields = [ 'name', 'internal_num', 'public_num', 'is_published', 'pdf',  'views_count']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['internal_num', 'public_num']:
            self.fields[field].widget.attrs.update({'class': 'border-success input-group-text rounded text-center col-sm-12 text-family'})
        self.fields['internal_num'].disabled = True
        self.fields['public_num'].disabled = True
        self.fields['views_count'].disabled = True
        self.fields['views_count'].widget.attrs.update({'class': 'border-success input-group-text rounded text-center col-sm-12'})
        self.fields['is_published'].widget.attrs.update({'class': 'border border-primary col-sm-1 float-left'})
        self.fields['pdf'].widget.attrs.update({'class': 'border border-primary text-family btn btn-outline-secondary m-auto'})
        self.fields['name'].widget.attrs.update({'class': 'border border-primary input-group-text rounded text-center text-family col-sm-12'})

class EditProfileForm(ModelForm):

    company_name = forms.CharField(empty_value="Company name", required=True)

    class Meta:
        model = CustomUser
        fields = [ 'company_name',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_name'].widget.attrs.update({'class': 'form-control-plaintext bg-success rounded h6'})
