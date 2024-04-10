from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('trigger_report', views.trigger_report, name='trigger_report'),
    path('get_report', views.get_report, name='get_report')
]