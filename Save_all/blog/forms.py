from django import forms
from django.forms import fields, widgets
from .models import Post, Comment

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control custom-text','cols':'40', 'rows':'4'}),label='')
    class Meta:
        model =Comment
        fields =['body',]

class PostCreateForm(forms.ModelForm):
    image = forms.ImageField(label='Загрузить картинку')

    class Meta:
        model = Post
        fields = ["title", "content", "image"]