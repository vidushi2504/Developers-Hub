from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
from .forms import PostForm, UpdateForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .models import Post, Comment, Category
# Create your views here.

def home(request):
	posts=Post.objects.all()
	context = {
		'posts': posts,
	}
	return render(request, 'home/home.html', context)


class PostListView(ListView):
	model = Post
	template_name = 'home/home.html' #<app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	cats = Category.objects.all()
	ordering = ['-date_posted']	#newest to oldest

	def get_context_data(self, *args, **kwargs):
		cat_menu = Category.objects.all()
		context = super(PostListView, self).get_context_data(*args, **kwargs)
		context["cat_menu"] = cat_menu
		return context

class PostDetailView(DetailView):
	model = Post
	# template_name = 'home/post_detail.html'

	def get_context_data(self, *args, **kwargs):
		post_available = get_object_or_404(Post, id=self.kwargs['pk'])
		cat_menu = Category.objects.all()
		context = super(PostDetailView, self).get_context_data()
		context["cat_menu"] = cat_menu
		return context

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	form_class = UpdateForm

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author
		
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/home'

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

class AddCommentView(CreateView):
	model = Comment
	template_name = 'home/add_comment.html'
	fields = ['body']
	success_url = reverse_lazy('home')

	def form_valid(self, form):
		form.instance.post_id = self.kwargs['pk']
		form.instance.author = self.request.user
		return super().form_valid(form)


class AddCategoryView(CreateView):
	model = Category
	template_name = 'home/add_category.html'
	fields = ['name']
	success_url = reverse_lazy('home')

def CategoryView(request, cats):
	category_posts = Post.objects.filter(category = cats.replace('-', ' '))
	return render(request, 'home/categories.html', {'cats':cats.title().replace('-', ' '), 'category_posts':category_posts})

def CategoryListView(request):
	cat_menu_list = Category.objects.all()
	return render(request, 'home/category_list.html', {'cat_menu_list': cat_menu_list})
