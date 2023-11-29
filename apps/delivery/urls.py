#URLS
from django.urls import path
from django.views.generic import TemplateView
from . import views

from .views import CalculationListView, CalculationDetailView,  CalculationCreateView

urlpatterns = [
    path('', views.login_view, name='login'),
    path('base/', TemplateView.as_view(template_name='base.html')),
    path('client_list/', views.client_list, name='client_list'),
    path('add/', views.client_form, name='client_form'),
    path('client/<int:pk>/', views.client_edit, name='client_detail'),
    path('client/', views.client_list, name='client_list'),
    path('calculations/', CalculationListView.as_view(), name='calculation-list'),
    path('calculation/<int:pk>/', CalculationDetailView.as_view(), name='calculation_detail'),
    path("calculation-create", views.CalculationCreateView, name="calculation-create"),



        ]



