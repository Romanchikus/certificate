from django.db import models
from users.models import CustomUser
import uuid
from django.urls import reverse

import qrcode
from io import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError
from random import randrange

def user_directory_path(certificate, filename):
    # file will be uploaded to MEDIA_ROOT/public_num/<filename>
    return  f"user_{certificate.public_num}/{filename}"

def generate_random_unique_internal_num():
    random_number = randrange(1000)

    while Certificate.objects.filter(internal_num=random_number):
        random_number = randrange(1000)
    return random_number

class CertificateManager(models.Manager):

    def create(self, **obj_data):

        obj_data['qr_code'] = self.generate_qrcode(obj_data['public_num'])

        # Now call the super method which does the actual creation
        return super().create(**obj_data)
        

class Certificate(models.Model):

    name = models.CharField("name", max_length=50)
    emitter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    internal_num = models.CharField(max_length=50, default=generate_random_unique_internal_num)
    public_num = models.UUIDField(default=uuid.uuid4)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    is_published = models.BooleanField(default=False)
    pdf = models.FileField(upload_to=user_directory_path,blank=True, null=True)
    views_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ("emitter", "internal_num")
        constraints = [
            models.UniqueConstraint(fields=['emitter', 'internal_num'], name='unique emitter')
        ]

    def validate_unique(self,exclude=None):
        try:
            super(Certificate,self).validate_unique()
        except ValidationError as e:
            raise ValidationError("Internal num is not unique")

    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )
        qr.add_data(self.get_absolute_url())
        qr.make(fit=True)

        img = qr.make_image()

        buffer = StringIO.StringIO()
        img.save(buffer)
        filename = 'cert-%s.png' % (self.public_num)
        filebuffer = InMemoryUploadedFile(
            buffer, None, filename, 'image/png', buffer.len, None)
        self.qrcode.save(filename, filebuffer)
        return self.qrcode

    def __str__(self):
        return str(self.public_num)

    def get_absolute_url(self):
        return reverse('certificate_info', kwargs=[str(self.pk)])

