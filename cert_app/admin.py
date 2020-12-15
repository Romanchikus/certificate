from django.contrib import admin
from .models import Certificate

class CertificateAdmin(admin.ModelAdmin):

    fields = ('name' , 'internal_num', 'qr_code', 'is_published', 'pdf', 'emitter')
    list_display = ['id', 'public_num', 'name']

admin.site.register(Certificate, CertificateAdmin)