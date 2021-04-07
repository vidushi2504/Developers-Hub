from django.contrib import admin
from django.urls import path
from .views import (
	PostListView, 
	PostDetailView,
	PostCreateView,
	PostDeleteView,
	AddCommentView,
	AddCategoryView,
	CategoryView,
	CategoryListView,
	updatePost
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.updatePost, name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', AddCommentView.as_view(), name='add-comment'),
    path('add_category/', AddCategoryView.as_view(), name='add-category'),
    path('category/<str:cats>/', CategoryView, name='category'),
    path('category-list/', CategoryListView, name='category-list'),
]