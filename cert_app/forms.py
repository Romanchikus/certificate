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
