from django import forms
from .models import Post, Category

choices = Category.objects.all().values_list('name', 'name')

choice_list = []
for item in choices:
	choice_list.append(item)

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'snippet', 'content', 'category')

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'snippet': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter text snippet upto 200 words to be visible on home page....', 'rows':5, 'cols':90}),
			'content': forms.Textarea(attrs={'class': 'form-control'}),
			'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
		}

class UpdateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'snippet', 'content', 'category')

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'snippet': forms.Textarea(attrs={'class': 'form-control'}),
			'content': forms.Textarea(attrs={'class': 'form-control'}),
			'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
		}