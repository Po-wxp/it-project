# Generated by Django 2.1.5 on 2020-03-06 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capturer', '0047_remove_photo_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='Image',
            field=models.ImageField(default='', upload_to='upload_photos'),
            preserve_default=False,
        ),
    ]
