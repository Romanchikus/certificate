from django.urls import path
<<<<<<< HEAD
from .views import CreateCert, HomePageView, DetailsCertView, AddCertView, ListCertView, DeleteCertView, PublishCertView
=======
from .views import CreateCert, HomePageView, DetailsCertView, AddCertView, ListCertView, DeleteCertView
>>>>>>> 17e42b30322b87c5ff6aa1fcb1d70de35297c1c6

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('certificates', ListCertView.as_view(), name='list'),                         
    path('certificates/create',CreateCert.as_view(), name='create'),
    path('certificates/add/<int:pk>/', AddCertView.as_view(), name='add'),
    path('certificates/<int:pk>/', DetailsCertView.as_view(), name='detail'),
<<<<<<< HEAD
    path('certificates/publish/<int:pk>/', PublishCertView.as_view(), name='publish'),
=======
    path('certificates/<int:pk>/', AddCertView.publish, name='publish'),
>>>>>>> 17e42b30322b87c5ff6aa1fcb1d70de35297c1c6
    path('certificates/delete/<int:pk>/', DeleteCertView.as_view(), name='delete'),
]