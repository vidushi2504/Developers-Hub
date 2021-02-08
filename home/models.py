from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length = 100)
	content = models.TextField()
	date_posted = models.DateTimeField(default = timezone.now)
	author = models.ForeignKey(User, on_delete= models.CASCADE)
	likes = models.ManyToManyField(User, related_name = 'blog_posts')
	#done
	#assigned to
	#category

	def total_likes(self):
		return self.likes.count()

	def __str__(self):
		return self.title + ' | ' + str(self.author)

	def get_absolute_url(self):
		return reverse('home')

class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments', on_delete= models.CASCADE)
	name = models.CharField(max_length=255)
	body = models.TextField()
	date_added = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return self.post.title + ' | ' + str(self.name)
			
