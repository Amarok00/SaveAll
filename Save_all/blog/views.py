import random
from typing import Any, Dict, Optional

from blog.models import Comment, Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

# from django.urls.base import reverse_lazy
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CommentForm

def index(request):
    context = {"posts": Post.objects.all()}
    return render(request, "blog/index.html", context)


@login_required
def posts_of_following_profiles(request):
    pass


@login_required
def LikeView(request):
    pass


@login_required
def SaveView(request):
    pass

def save_post_if_ajax(request):
    post = get_object_or_404(Post, id = request.POST.get("id"))
    saved = False
    if post.saves_posts.filter(id=request.user.id).exists():
        post.saves_posts.remove(request.user)
        saved = False
    else:
        post.saves_posts.add(request.user)
        saved = True
    context = {
        'post':post,
        'total_saves':post.total_saves_posts(),
        'saved': saved
    }
    if request.is_ajax:
        html = render_to_string('blog/save_section.html',context,request=request)
        return JsonResponse({'form':html})

@login_required
def LikeCommentView(request):  
    pass


class WorldPostListViewAllUser(ListView):
    model = Post
    template_name = "blog/world.html"
    context_object_name = "posts"
    ordering = ["-data_create"]
    paginate_by = 3

    
    def get_context_data(self, *args, **kwargs):
        context = super(WorldPostListViewAllUser, self).get_context_data()
        users = list(User.objects.exclude(pk=self.request.user.pk))
        if len(users) > 3:
            out = 3
        else:
            out = len(users)
        random_users = random.sample(users, out)
        context["random_users"] = random_users
        return context


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "blog_post_user_list"
    paginate_by = 2
    # def get_queryset(self) -> QuerySet[Any]:
    #     user = get_object_or_404(User,username= self.kwargs.get('username'))
    #     return Post.objects.filter(author=user).order_by("-data_create")

    def get_queryset(self) -> QuerySet[Any]:
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-data_create")


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def post_detail_view(request, slug, pk):
    handle_page = get_object_or_404(Post, slug=slug, id=pk)
    total_comments = (
        handle_page.comments_blog.all().filter(reply_comment=None).order_by("-id")
    )
    total_comments2 = handle_page.comments_blog.all().order_by("-id")
    total_likes = handle_page.total_likes_post()
    total_saves = handle_page.total_saves_posts()

    context = {}
    if request.method == "POST":
        comment_qs = None
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            form = request.POST.get("body")
            comment = Comment.objects.create(
                name_author=request.user,
                body=form,
                post=handle_page,
                reply_comment=comment_qs,
            )
            comment.save()
            total_comments = (
                handle_page.comments_blog.all()
                .filter(reply_comment=None)
                .order_by("-id")
            )
    else:
        comment_form = CommentForm()

    liked = False  
    if  handle_page.likes_post.filter(id=request.user.id).exists():
        liked = True
    context['total_likes'] = total_likes
    context['liked'] = liked 

    saved = False
    if handle_page.saves_posts.filter(id=request.user.id).exists():
        saved = True
    context['total_saves'] = total_saves
    context['saved'] = saved
    context["comment_form"] = comment_form
    context["comments"] = total_comments
    context["post"] = handle_page
    if request.is_ajax:
        html = render_to_string("blog/comments.html", context,request=request)
        return JsonResponse({'form': html})
    return render(request, "blog/post_detail.html", context)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"
    template_name = "blog/delete_post.html"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def all_save_view_posts(request):
    user = request.user
    saved_posts = user.blog_posts_save.all()
    context = {'saved_posts':saved_posts}
    return render(request,'blog/saved_posts.html',context) 

@login_required
def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    liked = False
    if post.likes_post.filter(id=request.user.id).exists():
        post.likes_post.remove(request.user)
        liked = False
        #notify = Notification.objects.filter(post=post, sender=request.user, notification_type=1)
        #notify.delete()
    else:
        post.likes_post.add(request.user)
        liked = True
        #notify = Notification.objects.filter(post=post, sender=request.user, user= post.author,   notification_type=1)
        #notify.save()
    context = {
        'post': post,
        'total_likes' : post.total_likes_post(),
        'liked' : liked,
        
    }
    
    if request.is_ajax:
        html = render_to_string('blog/like_section.html',
                                context,
                                request=request)
                                
    return JsonResponse({'form': html})