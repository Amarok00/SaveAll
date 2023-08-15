# Generated by Django 4.2.4 on 2023-08-13 12:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0010_remove_post_likes_remove_post_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes_post',
            field=models.ManyToManyField(blank=True, related_name='postcomment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='saves_posts',
            field=models.ManyToManyField(blank=True, related_name='blog_posts_save', to=settings.AUTH_USER_MODEL, verbose_name='Сохранённые посты пользователя'),
        ),
    ]
