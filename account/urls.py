from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<int:userid>', views.user_account, name='account'),
    path('creation', views.user_creation, name='creation'),
    path('editdetails', views.edit_details, name='editdetails'),
]