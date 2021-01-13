from django import forms
from django.forms import ModelForm

from .models import Post
from .models import Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["group", "text", "image"]
        widgets = {
            "text": forms.Textarea()
        }


class FormComments(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea()
        }
