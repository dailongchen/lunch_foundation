from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('last', views.last, name='last'),
    path('members', views.members, name='members'),
    path('this_week', views.this_week, name='this_week'),
    path('this_month', views.this_month, name='this_month'),
    path('this_year', views.this_year, name='this_year'),
    path('new_report', views.new_report, name='new_report'),
]