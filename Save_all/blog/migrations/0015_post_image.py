# Generated by Django 4.2.4 on 2023-08-20 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='Save_all/other_static/bootstrap5/assets/img/pixlr-bg.png', upload_to='post_images/'),
        ),
    ]