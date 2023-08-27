from django.apps import AppConfig
from django.db.models.signals import post_save

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from users.signals import create_profile
        from django.contrib.auth.models import User
        post_save.connect(create_profile, sender=User)
        from users.signals import save_profile
        post_save.connect(save_profile, sender=User)