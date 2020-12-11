from django.contrib import admin
from .models import Certificate

class CertificateAdmin(admin.ModelAdmin):

    fields = ('name' , 'internal_num', 'qr_code', 'status', 'pdf')

admin.site.register(Certificate, CertificateAdmin)