# Generated by Django 2.1.5 on 2020-02-27 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('capturer', '0029_auto_20200227_0417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favoritephoto',
            name='favorite',
        ),
        migrations.RemoveField(
            model_name='favoritephoto',
            name='user',
        ),
        migrations.DeleteModel(
            name='FavoritePhoto',
        ),
    ]
