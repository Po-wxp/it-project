# Generated by Django 2.1.5 on 2020-03-13 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capturer', '0052_auto_20200307_2303'),
    ]

    operations = [
        migrations.CreateModel(
            name='temp_photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='template/')),
            ],
        ),
    ]