from django.urls import path, re_path
from blog.views import (
    UserPostListView,
    PostCreateView,
    post_detail_view,
    PostDeleteView,
    PostUpdateView,
    WorldPostListViewAllUser,
    all_save_view_posts,
    save_post_if_ajax,
    LikeCommentView,
)
from . import views

urlpatterns = [
    path("world/", WorldPostListViewAllUser.as_view(), name="blog-world"),
    path("", views.index, name="index-home"),
    path("about/", views.about, name="about"),
    path(
        "posts/user/<str:username>/", UserPostListView.as_view(), name="user-posts-list"
    ),
    path(
        "posts/<str:slug>/<int:pk>/detail/", views.post_detail_view, name="post-detail"
    ),
    path("post/like/", views.like_post, name="post-like"),
    path("posts/new/", PostCreateView.as_view(), name="post-create"),
    path("post/save/", views.save_post_if_ajax, name="post-save"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("posts/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("saved-posts/", views.all_save_view_posts, name="all-save"),
    path("comment-like/", LikeCommentView.as_view(), name="comment-like"),
]
