from django.urls import path
from .views import HomePageView, CreateCertView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('certificates/add', CreateCertView.as_view(), name='add'),
]