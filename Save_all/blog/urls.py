
from django.urls import path, re_path
from blog.views import  UserPostListView, PostCreateView,PostDetailView, PostDeleteView, PostUpdateView
from . import views

urlpatterns = [
    path('',views.index,name='index-home'),
    path('posts/user/<str:username>/',UserPostListView.as_view() , name='user-posts-list' ),
    path('posts/new/',PostCreateView.as_view() , name='post-create' ),
    path('posts/<int:pk>/delete/',PostDeleteView.as_view() , name='post-delete' ),
    path('posts/<int:pk>/update/',PostUpdateView.as_view() , name='post-update' ),
    path('posts/<slug:slug>/<int:pk>/detail/',PostDetailView.as_view() , name='post-detail' ),
]