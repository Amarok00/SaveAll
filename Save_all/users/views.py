from django.shortcuts import render, reverse, redirect
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
            'post_form': post_form,
            'comment_form': comment_form,
            'posts': posts,
            'edit_profile_form': edit_profile_form,
            'edit_image_form': edit_image_form,
            'user_profile': request.user.profile,
        }
        return render(request, 'users/profile.html', context)


class UserProfileView(View):

    def get(self, request, username, *args, **kwargs):
        user_profile = Profile.objects.get(user__username=username)
        if user_profile.user == request.user:
            return HttpResponseRedirect(reverse('profile'))
        post_form = PostCreateForm()
        comment_form = CommentForm()
        posts = user_profile.posts.all()
        context = {
            'post_form': post_form,
            'comment_form': comment_form,
            'posts': posts,
            'user_profile': user_profile,
        }
        return render(request, 'users/user_profile.html', context)


class EditImageAjaxView(View):

    def post(self, request, *args, **kwargs):
        user = request.user
        new_image = request.FILES['image']
        user.profile.image = new_image
        user.profile.save()
        image_url = user.profile.image.url
        return JsonResponse({'success': True, 'image_url': image_url})


class EditProfileView(View):

    def get(self, request, *args, **kwargs):
        profile_form = EditProfileInfoForm(instance=request.user.profile)
        password_form = PasswordChangeForm(user=request.user)
        password_form.fields['old_password'].widget.attrs['autofocus'] = False

        image_form = ChangeImageForm(instance=request.user.profile)
        context = {
            'profile_form': profile_form,
            'password_form': password_form,
            'image_form': image_form,
        }
        return render(request, 'users/edit_profile.html', context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            profile_form = EditProfileInfoForm(
                request.POST, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                return JsonResponse({'success': True}) and redirect('/profile/')
            return JsonResponse(
                {'success': False, 'errors': profile_form.errors}
            )




class ResetImageView(View):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            user = request.user
            user.profile.image = None
            user.profile.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class DeleteUserView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            user.delete()
            return redirect('/')