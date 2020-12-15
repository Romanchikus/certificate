from django.shortcuts import render
from .models import Certificate
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView, DeleteView, View
from .forms import PreCertificate
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from users.models import CustomUser

from django.http import  HttpResponseRedirect

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
    fields = ['name', 'is_published', 'pdf', 'internal_num']

    def get_success_url(self):
        return reverse('list_of_certificates')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.object
        return context


class DetailsCertificateView(DetailView):

    template_name = 'certificate/detail.html'
    model = Certificate

    def dispatch(self, request, *args, **kwargs):
        cert = Certificate.objects.filter(pk=kwargs["pk"]).first()
        cert.views_count +=1
        cert.save()
        return super().dispatch(request, *args, **kwargs)


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