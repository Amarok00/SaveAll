from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from blog.forms import PostCreateForm, CommentForm
from .forms import EditProfileInfoForm, ChangeImageForm

from .models import Profile


class MyProfileView(View):
    def get(self, request, *args, **kwargs):
        post_form = PostCreateForm()
        comment_form = CommentForm()
        posts = Profile.objects.get(user=request.user).posts.all()
        edit_profile_form = EditProfileInfoForm(instance=request.user.profile)
        edit_image_form = ChangeImageForm(instance=request.user.profile)
        context = {
            "post_form": post_form,
            "comment_form": comment_form,
            "posts": posts,
            "edit_profile_form": edit_profile_form,
            "edit_image_form": edit_image_form,
            "user_profile": request.user.profile,
        }
        return render(request, "users/profile.html", context)


class UserProfileView(View):
    def get(self, request, username, *args, **kwargs):
        user_profile = get_object_or_404(Profile, user__username=username)

        if user_profile.user == request.user:
            return HttpResponseRedirect(reverse("profile"))

        post_form = PostCreateForm()
        comment_form = CommentForm()
        posts = user_profile.posts.all()

        context = {
            "post_form": post_form,
            "comment_form": comment_form,
            "posts": posts,
            "user_profile": user_profile,
        }

        return render(request, "users/user_profile.html", context)


class EditProfileView(View):

    def get(self, request, *args, **kwargs):
        profile_form = EditProfileInfoForm(instance=request.user.profile)
        password_form = PasswordChangeForm(user=request.user)
        password_form.fields["old_password"].widget.attrs["autofocus"] = False

        image_form = ChangeImageForm(instance=request.user.profile)
        context = {
            "profile_form": profile_form,
            "password_form": password_form,
            "image_form": image_form,
        }
        return render(request, "users/edit_profile.html", context)

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            # Get the profile instance for the current user
            profile_instance = get_object_or_404(Profile, user=request.user)
            print(f"Current User: {request.user}")
            print(f"Profile Instance User: {profile_instance.user}")

            # Initialize both forms with the correct instance
            profile_form = EditProfileInfoForm(request.POST, instance=profile_instance)
            image_form = ChangeImageForm(
                request.POST, request.FILES, instance=profile_instance
            )

            # Check if both forms are valid
            if profile_form.is_valid() and image_form.is_valid():
                # Save changes for both forms
                profile_form.save()
                image_form.save()
                print("Changes saved successfully.")
                return JsonResponse({"success": True})
            else:
                # If there are validation errors, return the errors in the response
                errors = {
                    "profile_errors": profile_form.errors.as_json(),
                    "image_errors": image_form.errors.as_json(),
                }
                print(f"Validation Errors: {errors}")
                return JsonResponse({"success": False, "errors": errors})


class ResetImageView(View):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            user = request.user
            user.profile.image = None
            user.profile.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})


class DeleteUserView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            user.delete()
            return redirect("/")


class CheckUserOnlineStatusView(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            username = request.GET.get("username")
            user = User.objects.get(username=username)
            return JsonResponse({"online": user.profile.online})
        return JsonResponse({"success": False})
