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
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from .models import Post, Comment, Category, User
from account.models import Experience, Account
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
	posts=Post.objects.all()
	context = {
		'posts': posts,
	}
	return render(request, 'home/home.html', context)

class PostListView(ListView):
	model = Post
	template_name = 'home/home.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	cats = Category.objects.all()
	ordering = ['-date_posted']	# newest to oldest

	def get_context_data(self, *args, **kwargs):
		top_people=Account.objects.order_by('-reputation_points')[:5]
		cat_menu = Category.objects.all()
		context = super(PostListView, self).get_context_data(*args, **kwargs)
		context["cat_menu"] = cat_menu
		context['top_people']=top_people
		return context

class PostDetailView(DetailView):
	model = Post
	context_object_name = 'post'

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

# class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
# 	model = Post
# 	form_class = UpdateForm

# 	def form_valid(self, form):
# 		form.instance.author = self.request.user
# 		return super().form_valid(form)

# 	def test_func(self):
# 		post = self.get_object()
# 		return self.request.user == post.author
		
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/home'

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

class AddCommentView(LoginRequiredMixin, CreateView):
	model = Comment
	template_name = 'home/add_comment.html'
	fields = ['body']
	success_url = reverse_lazy('home')

	def form_valid(self, form):
		form.instance.post_id = self.kwargs['pk']
		form.instance.author = self.request.user
		return super().form_valid(form)

class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Comment
	success_url = '/home'

	def test_func(self):
		post = self.get_object()

		return self.request.user == post.author

class AddCategoryView(LoginRequiredMixin, CreateView):
	model = Category
	template_name = 'home/add_category.html'
	fields = ['name']
	success_url = reverse_lazy('home')

@login_required
def CategoryView(request, cats):
	category_posts = Post.objects.filter(category = cats.replace('-', ' '))
	return render(request, 'home/categories.html', {'cats':cats.title().replace('-', ' '), 'category_posts':category_posts})

@login_required
def CategoryListView(request):
	cat_menu_list = Category.objects.all()
	return render(request, 'home/category_list.html', {'cat_menu_list': cat_menu_list})

@login_required
def updatePost(request, pk):
	post=Post.objects.filter(id=pk)[0]
	potential_mentors=Comment.objects.filter(post=post)
	categories=Category.objects.all()

	if request.method=='POST':
		getTitle=request.POST.get('title', '')
		post.title=getTitle
		post.content=request.POST.get('content', '')
		post.category=request.POST.get('category', '')
		mentorUsername=request.POST.get('mentor', '')

		if mentorUsername!="Choose a mentor" :
			getMentor=User.objects.filter(username=mentorUsername)[0]
			post.assign_to=getMentor

		check=request.POST.get('complete', False)
		if check: 
			post.done=True
			if mentorUsername!="Choose a mentor" :
				obj=Experience(user=getMentor, title=getTitle, startdate=post.date_posted.date(), enddate=datetime.datetime.now().date())
				acc=Account.objects.filter(user=getMentor)[0]
				acc.reputation_points+=200
				acc.save()
				obj.save()
		post.save()
		return redirect('post-detail', pk=pk)

	context={
		'obj': post,
		'mentors': potential_mentors, 
		'categories': categories,
	}
	return render(request, 'home/postUpdate.html', context) 

@login_required
def search(request):
	query = request.GET['query']
	if len(query)>80:
		posts=[]
	else:
		poststitle = Post.objects.filter(title__icontains = query)
		postscontent = Post.objects.filter(content__icontains=query)
		posts = postscontent.union(poststitle)
	context = {'posts':posts, 'query':query}
	return render(request, 'home/search.html', context)
