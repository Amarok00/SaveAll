
from django.urls import path, re_path
from blog.views import  UserPostListView, PostCreateView,PostDetailView

urlpatterns = [
    path('posts/user/<str:username>/',UserPostListView.as_view() , name='user-posts-list' ),
    path('posts/new/',PostCreateView.as_view() , name='post-create' ),
    path('posts/<slug:slug>/<int:pk>/detail/',PostDetailView.as_view() , name='post-detail' ),
]