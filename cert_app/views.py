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


class CreateCert(View):

    def post(self, request):
        id=request.user.id
        user = CustomUser.objects.get(id=id)
        model = Certificate(emitter= user)
        model.save()
        print(model.id)
        return HttpResponseRedirect(reverse("add",
                                        kwargs={'pk':model.pk},
                                    )
                            )


class AddCertView(UpdateView):

    template_name = 'certificate/add.html'
    model = Certificate
    fields = ['name', 'status', 'pdf', 'internal_num']

    def get_success_url(self):
        return reverse('list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.object
        return context
    
    def form_valid(self, form, status=False):
        form.instance.status = status
        return super().form_valid(form)

    def publish(self):
        pass


class DetailsCertView(DetailView):

    template_name = 'certificate/detail.html'
    model = Certificate

    def dispatch(self, request, *args, **kwargs):
        cert = Certificate.objects.filter(pk=kwargs["pk"]).first()
        cert.reviews +=1
        cert.save()
        return super().dispatch(request, *args, **kwargs)


class ListCertView(ListView):

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
    

class SearchCertView(ListView):

    model = Certificate
    template_name = 'certificate/list.html'
    
    def get_queryset(self):
        name = self.request.GET.get('name', '')
        inter_num = self.request.GET.get('inter_num', None)
        qs =  Certificate.objects.all().filter(emitter=self.request.user)
        if name:
            qs = qs.filter(name__icontains=name)
        if inter_num:
            qs = qs.filter(internal_num__icontains=inter_num)
        return qs


class DeleteCertView(DeleteView):
    model = Certificate
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy("list")