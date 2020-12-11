from django.shortcuts import render
from .models import Certificate
from django.views.generic import TemplateView, CreateView

class HomePageView(TemplateView):
    
    template_name = 'home.html'

class CreateCertView(CreateView):

    template_name = 'certificate/create.html'
    model = Certificate
