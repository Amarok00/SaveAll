from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from .models import Profile

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Replace with the name of your login template
    success_url = '/index/'  # Replace with the desired URL after successful login

    def form_valid(self, form):
        # Perform any additional logic after successful login
        # For example, update the user's online status
        user = form.get_user()
        try:
            profile = Profile.objects.get(user=user)
            profile.is_online = True
            profile.save()
        except Profile.DoesNotExist:
            pass
        return redirect(self.get_success_url())
# Create your views here.
