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


class CreateCart(View):

    def post(self, request):
        id=request.user.id
        user = CustomUser.objects.get(id=id)
        model = Certificate(internal_num= user)
        model.save()
        print(model.id)
        return HttpResponseRedirect(reverse("add",
                                        kwargs={'pk':model.pk},
                                    )
                            )


class AddCertView(UpdateView):

    template_name = 'certificate/add.html'
    model = Certificate
    fields = ['name', 'status', 'pdf']

    def get_success_url(self):
        return reverse('list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.object
        return context
    


class DetailsCertView(DetailView):

    template_name = 'certificate/add.html'
    model = Certificate


class ListCertView(ListView):

    template_name = 'certificate/list.html'
    model = Certificate

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kwargs["cert_form"] = PreCertificate(
            initial={ "internal_num": self.request.user}
        )
        return context
    

    def get_queryset(self, **kwargs):
        kwargs["cert_form"] = PreCertificate(
            initial={ "internal_num": self.request.user}
        )
        return self.model.objects.filter(internal_num=self.request.user)
    

class DeleteCertView(DeleteView):
    model = Certificate
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy("list")