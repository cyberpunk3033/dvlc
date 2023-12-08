#URLS

from django.urls import path, include, re_path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('base/', TemplateView.as_view(template_name='base.html')),
    path('client_list/', views.client_list, name='client_list'),
    path('add/', views.client_form, name='client_form'),
    path('client/<int:pk>/', views.client_edit, name='client_detail'),
    path('client/', views.client_list, name='client_list'),
    path('calculations/', views.calc_list_view.as_view(), name='calculation-list'),
    path('calculation/<int:pk>/', views.calc_list_detail_view.as_view(), name='calculation_detail'),
    path('calculation-create/', views.calc_list_create_view, name='calculation-create'),
    # path('autocomplete/', views.CalculationCreateView, name='autocomplete'),

    path('search/', views.search_client_view, name='search_view'),
    path('search/results/', views.search_client_results_view, name='search_results_view'),
    path('home/', views.autocomplete, name='autocomplete'),


        ]



