from django.urls import path
from . import views
urlpatterns = [
    path('', views.hi, name='home-page'),
    path('input', views.input, name='index'),
    path('export', views.export, name='export'),
]