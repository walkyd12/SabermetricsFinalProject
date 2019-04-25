from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:teamID>', views.team, name='team')
]