from django.urls import path
from .views import (CreateCertificateView, HomePageView, DetailsCertificateView, AddCertificateView, 
ListCertificateView, DeleteCertificateView, SearchCertificateView, FoundCertificateView, ProfileView,
PublishCertificateView)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('certificates', ListCertificateView.as_view(), name='list_of_certificates'),                         
    path('certificates/create',CreateCertificateView.as_view(), name='create_certificate'),
    path('certificates/add/<int:pk>/', AddCertificateView.as_view(), name='add_certificate'),
    path('certificates/publish/<int:pk>/', PublishCertificateView.as_view(), name='publish_certificate'),
    path('certificates/<int:pk>/', DetailsCertificateView.as_view(), name='certificate_info'),
    path('detail', FoundCertificateView.as_view(), name='check_certificate'),
    path('certificates/delete/<int:pk>/', DeleteCertificateView.as_view(), name='delete_certificate'),
    path('certificates/search', SearchCertificateView.as_view(), name='search_certificates'),
    path('profile/', ProfileView.as_view(), name='profile'),
]