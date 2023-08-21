from django.contrib import admin
from users.models import Profile
# Register your models here.

@admin.register(Profile)
class PageAdmin(admin.ModelAdmin):
    list_display = ['user']