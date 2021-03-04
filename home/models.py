from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField


class Category(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('home')

class Post(models.Model):
	title = models.CharField(max_length = 100)
	snippet = models.CharField(max_length= 200)
	content = RichTextField(blank=True, null=True)
	date_posted = models.DateTimeField(default = timezone.now)
	author = models.ForeignKey(User, on_delete= models.CASCADE)
	category = models.CharField(max_length=255, default='Coding')
	#done
	#assigned to

	def __str__(self):
		return self.title + ' | ' + str(self.author)

	def get_absolute_url(self):
		return reverse('home')

class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments', on_delete= models.CASCADE)
	name = models.CharField(max_length=255, default='user')
	body = models.TextField()
	date_added = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return self.post.title + ' | ' + str(self.name)


# class Comment(models.Model):
# 	post = models.ForeignKey(Post, related_name='comments', on_delete= models.CASCADE)
# 	author = models.ForeignKey(User, on_delete= models.CASCADE, default=1)
# 	body = models.TextField()
# 	date_added = models.DateTimeField(default = timezone.now)

# 	def __str__(self):
# 		return self.post.title + ' | ' + str(self.name)