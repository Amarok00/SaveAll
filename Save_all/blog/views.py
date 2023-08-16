from typing import Any, Optional
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView,CreateView,DetailView,DeleteView, UpdateView
from django.contrib.auth.models import User
# from django.urls.base import reverse_lazy
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from blog.models import Post 

def index(request):
    context = {
        'posts':Post.objects.all()
    }
    return render(request,'blog/index.html',context)


@login_required
def posts_of_following_profiles(request):
    pass


@login_required
def LikeView(request):
    pass


@login_required
def SaveView(request):
    pass


@login_required
def LikeCommentView(request): # , id1, id2              id1=post.pk id2=reply.pk
    pass


class PostListView(ListView):
    pass


class UserPostListView(ListView):
    model = Post 
    template_name = "blog/user_posts.html"
    # context_object_name = "blog_post_user_list"

    # def get_queryset(self) -> QuerySet[Any]:
    #     user = get_object_or_404(User,username= self.kwargs.get('username'))
    #     return Post.objects.filter(author=user).order_by("-data_create")
    
    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = Post.objects.filter(author=user)  
        context = super().get_context_data(**kwargs)
        context['blog_post_user_list'] = queryset.order_by('-data_create')
        return context

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post 
    fields = ['title','content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# class PostDetailView(DetailView):
#     model = Post
#     # template_name = "blog/post_detail.html"
#     context_object_name = 'blog_post_detail'

def PostDetailView(request, slug, pk):
    handle_page = get_object_or_404(Post,slug=slug ,id=pk )
    total_comments = handle_page.comments_blog.all().filter(reply_comment=None).order_by('-id')
    total_comments2 = handle_page.comments_blog.all().order_by('-id')
    total_likes = handle_page.total_likes_post()
    total_save = handle_page.total_saves_posts()
    


    context = {}
    context['post'] = handle_page
    return render(request, 'blog/post_detail.html', context)

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/delete_post.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post 
    fields = ['title','content']

    def form_valid(self, form) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form) 
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False