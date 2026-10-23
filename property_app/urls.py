from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('health/', views.health_check_view, name='health_check'),
    path('suites/<slug:slug>/', views.suite_detail_view, name='suite_detail'),
    path('inquire/submit/', views.inquiry_submit_view, name='inquiry_submit'),
    path('contact/whatsapp/', views.quick_whatsapp_redirect, name='whatsapp_redirect'),
]
