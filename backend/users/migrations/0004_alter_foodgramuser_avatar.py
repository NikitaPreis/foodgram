# Generated by Django 3.2 on 2024-06-14 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_foodgramuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodgramuser',
            name='avatar',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='users/'),
        ),
    ]
