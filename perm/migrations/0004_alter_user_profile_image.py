# Generated by Django 5.0.7 on 2024-08-03 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perm', '0003_alter_user_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_images/default.png', null=True, upload_to='profile_images'),
        ),
    ]
