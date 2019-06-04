from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('id', 'message')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'name', 'desc', 'photo', 'tags')
