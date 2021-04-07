from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<int:userid>', views.user_account, name='account'),
    path('creation', views.user_creation, name='creation'),
    path('editdetails', views.edit_details, name='editdetails'),
    path('viewposts/<int:userid>/', views.view_posts, name='viewposts'),
    path('addexperince', views.add_experience, name="addexperience"),
]