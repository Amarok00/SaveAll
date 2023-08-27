from django.urls import path
from . import views
from .views import (
    MyProfileView,
    UserProfileView,
    EditImageAjaxView,
    EditProfileView,
    ResetImageView,
    DeleteUserView
)

urlpatterns = [
    path('profile/', MyProfileView.as_view(), name='profile'),
    path('profile/edit_avatar/',
        EditImageAjaxView.as_view(), name='edit_image_ajax'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/reset_image/',
        ResetImageView.as_view(), name='reset-image'),
    path('profile/delete/', DeleteUserView.as_view(), name='delete-user'),
    path('<str:username>/', UserProfileView.as_view(), name='user_profile'),
]