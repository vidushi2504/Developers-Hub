from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
	ListView, 
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .models import Post
# Create your views here.

def home(request):
	context = {
		'posts': Post.objects.all()
	}
	return render(request, 'home/home.html', context)

class PostListView(ListView):
	model = Post
	template_name = 'home/home.html' #<app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ['-date_posted']	#newest to oldest

class PostDetailView(DetailView):
	model = Post
	# template_name = 'home/post_detail.html'

	def get_context_data(self, *args, **kwargs):
		post_available = get_object_or_404(Post, id=self.kwargs['pk'])
		total_likes = post_available.total_likes()
		context = super(PostDetailView, self).get_context_data()
		context["total_likes"] = total_likes
		return context
	

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

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


def PostLikeView(request, pk):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	post.likes.add(request.user)
	return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


