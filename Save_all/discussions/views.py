from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from discussions.models import Discussions
from .forms import DiscussionsCreateForm


class UserDiscussionsListView(ListView):
    model = Discussions
    template_name = "blog/user_Discussions.html"
    # context_object_name = "blog_post_user_list"

    # def get_queryset(self) -> QuerySet[Any]:
    #     user = get_object_or_404(User,username= self.kwargs.get('username'))
    #     return Post.objects.filter(author=user).order_by("-data_create")

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        queryset = Discussions.objects.filter(author=user)
        context = super().get_context_data(**kwargs)
        context["blog_discussions_user_list"] = queryset.order_by("-data_create")
        return context


class DiscussionsCreateView(LoginRequiredMixin, CreateView):
    model = Discussions
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DiscussionsDetailView(DetailView):
    model = Discussions
    # template_name = "blog/post_detail.html"
    context_object_name = "discussions_discussions_detail"


@login_required
def discussions_create(request):
    form = DiscussionsCreateForm()
    if request.method == "POST":
        form = DiscussionsCreateForm(request.POST, request.FILES)

        if form.is_valid():
            new_discussion = form.save(commit=False)
            new_discussion.author = request.user
            new_discussion.save()
            messages.success(request, 'Дискуссия успешно добавлена')
            return redirect(new_discussion.get_absolute_url())
    return render(request, "discussions/create_form.html", {"form": form})