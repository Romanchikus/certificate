from django.contrib import admin
from .models import Certificate

class CertificateAdmin(admin.ModelAdmin):

    fields = ('name' , 'status', 'pdf')

admin.site.register(Certificate, CertificateAdmin)