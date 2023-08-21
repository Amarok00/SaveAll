from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.views import LoginView
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        profile.date_of_birth = request.POST.get('date_of_birth', '')
        profile.save()
        return redirect('profile')
    else:
        context = {'profile': profile}
        return render(request, 'users/profile.html', context)