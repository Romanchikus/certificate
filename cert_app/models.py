from django.db import models
from users.models import CustomUser
import uuid
from django.urls import reverse

import qrcode
from io import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/public_num/<filename>
    return 'user_{0}/{1}'.format(instance.public_num, filename)

class Certificate(models.Model):

    name = models.CharField("name", max_length=50)
    internal_num = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    public_num = models.URLField(default=uuid.uuid4, editable=False)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    status = models.BooleanField(default=False)
    pdf = models.FileField(upload_to=user_directory_path, null=True)

    objects = CertificateManager()

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

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('certificates.details', args=[str(self.id)])

class CertificateManager(models.Manager):

    def generate_qrcode(self):
        