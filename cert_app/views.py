from django.shortcuts import render, redirect, get_object_or_404
from .models import Certificate
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView, DeleteView, View, FormView
from .forms import PreCertificate
from django.urls import reverse, reverse_lazy
from users.models import CustomUser
from django.http import Http404
from django.core.exceptions import ValidationError
from django.views.defaults import page_not_found
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import  HttpResponseRedirect
from . import forms

class HomePageView(TemplateView):
    
    template_name = 'home.html'


class CreateCertificateView(View):

    def post(self, request):
        id=request.user.id
        user = CustomUser.objects.get(id=id)
        model = Certificate(emitter= user)
        model.save()
        print(model.id)
        return HttpResponseRedirect(reverse("add_certificate",
                                        kwargs={'pk':model.pk},
                                    )
                            )


class AddCertificateView(UpdateView):

    template_name = 'certificate/add.html'
    model = Certificate
    form_class = PreCertificate
    readonly_fields=('public_num',)

    def get_success_url(self):
        return reverse('list_of_certificates')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.object
        return context


class DetailsCertificateView(DetailView):

    template_name = 'certificate/detail.html'
    model = Certificate

    def get_object(self, queryset=None):
        if self.request.GET.get('check'):
            cert = get_object_or_404( Certificate, public_num=self.request.GET.get('public_num'))
        else:
            cert = Certificate.objects.get(pk=self.kwargs["pk"])
        cert.views_count +=1
        cert.save()
        return cert


class ListCertificateView(ListView):

    template_name = 'certificate/list.html'
    model = Certificate

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kwargs["cert_form"] = PreCertificate(
            initial={ "emitter": self.request.user}
        )
        return context
    

    def get_queryset(self, **kwargs):
        kwargs["cert_form"] = PreCertificate(
            initial={ "emitter": self.request.user}
        )
        return self.model.objects.filter(emitter=self.request.user)
    

class SearchCertificateView(ListView):

    model = Certificate
    template_name = 'certificate/list.html'
    
    def get_queryset(self):
        request = self.request.GET.get
        name =request('name')
        inter_num = request('inter_num')
        qs =  Certificate.objects.all().filter(emitter=self.request.user)
        if name:
            qs = qs.filter(name__icontains=name)
        if inter_num:
            qs = qs.filter(internal_num__icontains=inter_num)
        return qs


class DeleteCertificateView(DeleteView):
    model = Certificate
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy("list_of_certificates")


class FoundCertificateView(View):
    
    def dispatch(self, request, *args, **kwargs):
        public_num = self.request.GET.get('public_num')   
        try:
            cert =  get_object_or_404(Certificate, public_num=public_num)
        except ValidationError:
            raise Http404("Poll does not exist") 
        
        return redirect('certificate_info', pk=cert.pk)


def handler_404(request, exception):
    return page_not_found(request, exception, template_name="404.html")

class ProfileView(LoginRequiredMixin,  UpdateView):
    template_name = 'certificate/profile.html'
    model = CustomUser
    form_class = forms.EditProfileForm
    success_url = reverse_lazy('profile')
    

    def get_object(self, queryset=None):
        return self.request.user