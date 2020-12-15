from django.urls import path
from .views import CreateCert, HomePageView, DetailsCertView, AddCertView, ListCertView, DeleteCertView, SearchCertView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('certificates', ListCertView.as_view(), name='list'),                         
    path('certificates/create',CreateCert.as_view(), name='create'),
    path('certificates/add/<int:pk>/', AddCertView.as_view(), name='add'),
    path('certificates/<int:pk>/', DetailsCertView.as_view(), name='detail'),
    path('certificates/delete/<int:pk>/', DeleteCertView.as_view(), name='delete'),
    path('certificates/search', SearchCertView.as_view(), name='search'),
]