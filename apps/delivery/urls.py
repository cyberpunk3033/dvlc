#URLS
from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('base/', TemplateView.as_view(template_name='base.html')),
    path('client_list/', views.client_list, name='client_list'),
    path('add/', views.client_form, name='client_form'),
    path('client/<int:pk>/', views.client_edit, name='client_detail'),
    path('client/', views.client_list, name='client_list'),
    #path('client/search/', views.client_search, name='client_search'),
    # path('client/<int:pk>/edit/', views.client_edit, name='client_edit'),

          ]

