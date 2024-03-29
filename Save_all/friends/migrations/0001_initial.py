# Generated by Django 4.2.4 on 2024-02-15 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0006_profile_last_seen'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('accepted', models.BooleanField(default=False)),
                ('declined', models.BooleanField(default=False)),
                ('from_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_request_from_profile', to='users.profile')),
                ('to_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_request_to_profile', to='users.profile')),
            ],
        ),
    ]
