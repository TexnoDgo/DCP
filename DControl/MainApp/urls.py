from django.contrib import admin
from django.urls import path
from .views import detail_create, detail_all


urlpatterns = [
    path('AllDetail/', detail_all, name='detail_all'),
    path('Create', detail_create, name='detail_create'),
]
