from django.shortcuts import render
from .models import Certificate
from django.views.generic import TemplateView, CreateView, DetailView
from .forms import PreCertificate

class HomePageView(TemplateView):
    
    template_name = 'home.html'

class CreateCertView(CreateView):

    template_name = 'certificate/create.html'
    model = Certificate
    form_class = PreCertificate
    success_url = 'home'

class DetailsCertView(DetailView):

    emplate_name = 'certificate/detail.html'
    model = Certificate
    