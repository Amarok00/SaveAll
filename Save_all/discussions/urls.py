from django.urls import path, re_path
from discussions.views import (
    UserDiscussionsListView,
    DiscussionsCreateView,
    DiscussionsDetailView,
)
from discussions import views

urlpatterns = [
    path(
        "discussions/user/<str:username>/",
        UserDiscussionsListView.as_view(),
        name="user-discussions-list",
    ),
    # path(
    #     "discussions/new/", DiscussionsCreateView.as_view(), name="discussions-create"
    # ),
    path("create/", views.discussions_create, name="create"),
    path(
        "discussions/<slug:slug>/<int:pk>/detail/",
        DiscussionsDetailView.as_view(),
        name="discussions-detail",
    ),
]
