from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('battle/<int:first>/<int:second>/', views.battle, name="battle"),
    path('results', views.results, name="results"),
    path('upload/', views.upload, name="upload")
]
