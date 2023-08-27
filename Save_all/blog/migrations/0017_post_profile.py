# Generated by Django 4.2.4 on 2023-08-26 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_first_name_profile_last_name'),
        ('blog', '0016_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='users.profile'),
        ),
    ]