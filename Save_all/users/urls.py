from django.urls import path
from . import views
from .views import (
    MyProfileView,
    UserProfileView,
    EditProfileView,
    ResetImageView,
    DeleteUserView,
    CheckUserOnlineStatusView,
)

urlpatterns = [
    path("profile/", MyProfileView.as_view(), name="profile"),
    path("profile/edit/", EditProfileView.as_view(), name="edit_profile"),
    path("profile/delete/", DeleteUserView.as_view(), name="delete-user"),
    path("<str:username>/", UserProfileView.as_view(), name="user_profile"),
    path("check_online/", CheckUserOnlineStatusView.as_view(), name="check_online"),
]
