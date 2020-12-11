
from django.forms import ModelForm
from .models import Certificate
import uuid

class PreCertificate(ModelForm):

    class Meta:
        model = Certificate
        fields = '__all__'


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        user = kwargs.pop('user', None)
        self.fields['internal_num'].initial = user
        self.fields['public_num'] = uuid.uuid4()
        self.fields['qr_code'] = Certificate.generate_qrcode(self)