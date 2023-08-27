from django.contrib import admin
from users.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'first_name',
        'last_name',
        'bio',
        'friends_count',
    )
    list_filter = ['user',]

    def friends_count(self, obj):
        return obj.friends.count()
    friends_count.short_description = 'Friends count'