# Generated by Django 3.2 on 2024-07-04 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_auto_20240704_1342'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'default_permissions': ('add', 'change', 'delete', 'view'), 'default_related_name': 'recipe', 'ordering': ('-pub_date', 'name'), 'verbose_name': 'объект «Рецепт»', 'verbose_name_plural': '«Рецепты»'},
        ),
    ]
