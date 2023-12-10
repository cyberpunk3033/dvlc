#URLS
from dal import autocomplete
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from . import views
from django.urls import re_path as url

from .models import Calculation
from .views import calc_list_detail_view, calc_list_view

urlpatterns = [
    path('', views.login_view, name='login'),
    path('base/', TemplateView.as_view(template_name='base.html')),
    path('client_list/', views.client_list, name='client_list'),
    path('add/', views.client_form, name='client_form'),
    path('client/<int:pk>/', views.client_edit, name='client_detail'),
    path('client/', views.client_list, name='client_list'),
    path('calculations/', calc_list_view.as_view(), name='calculation-list'),
    path('calculation/<int:pk>/', calc_list_detail_view.as_view(), name='calculation_detail'),
    path("calculation-create", views.calc_list_create_view, name="calculation-create"),








        ]



