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
    

class PublishCertView(View):

    # model = Certificate
    # fields = ['name', 'status', 'pdf']

    # def form_valid(self, form):
    #     print('dfg')
    #     form.instance.status = True
    #     return super().form_valid(form)

    def post(self, request):
        id=request.POST['web_input']
        print(id)
        return super().post()




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
    

class DeleteCertView(DeleteView):
    model = Certificate
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy("list")